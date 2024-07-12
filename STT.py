from config import API_KEY, TEXT_FILE
from signal import SIGINT, SIGTERM
import asyncio
import sounddevice as sd
from concurrent.futures import ThreadPoolExecutor
from deepgram import (
    DeepgramClientOptions,
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)
is_finals = []


async def speech_to_text():
    global is_finals
    is_finals=[]
    try:
        loop = asyncio.get_event_loop()

        for signal in (SIGTERM, SIGINT):
            loop.add_signal_handler(
                signal,
                lambda: asyncio.create_task(
                    shutdown(signal, loop, dg_connection, stream)
                ),
            )

        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram = DeepgramClient(API_KEY, config)
        dg_connection = deepgram.listen.asynclive.v("1")

        async def send_to_deepgram(data):
            await dg_connection.send(data)

        def audio_callback(indata, frames, time, status, loop):
            if status:
                print(status)
            asyncio.run_coroutine_threadsafe(send_to_deepgram(indata.tobytes()), loop=loop)

        async def on_open(self, open, **kwargs):
            print(f"Connection Open")

        async def on_message(self, result, **kwargs):
            global is_finals
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if result.is_final:
                is_finals.append(sentence)
                utterance = " ".join(is_finals)
                print(f"Speech Final: {utterance}")
                if final_text_file:
                    final_text_file.write(utterance + "\n")
            else:
                print(f"Interim Results: {sentence}")

        async def on_metadata(self, metadata, **kwargs):
            print(f"Metadata: {metadata}")

        async def on_speech_started(self, speech_started, **kwargs):
            global final_text_file
            print(f"Speech Started")
            final_text_file = open(TEXT_FILE, "a")

        async def on_utterance_end(self, utterance_end, **kwargs):
            global is_finals
            print(f"Utterance End")
            if final_text_file:
                final_text_file.close()
            is_finals = []
            await shutdown(SIGINT, loop, dg_connection, stream)

        async def on_close(self, close, **kwargs):
            print(f"Connection Closed")

        async def on_error(self, error, **kwargs):
            print(f"Handled Error: {error}")

        async def on_unhandled(self, unhandled, **kwargs):
            print(f"Unhandled Websocket Message: {unhandled}")

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

        options = LiveOptions(
            model="nova-2-phonecall",
            language="en-US",
            smart_format=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            interim_results=True,
            utterance_end_ms="1500",  # Set to 2 seconds pause
            vad_events=True,
            endpointing=300,
            replace={"mail": "male"},
        )

        addons = {
            "no_delay": "true"
        }

        print("\n\nStart talking! Press Ctrl+C to stop...\n")
        if await dg_connection.start(options, addons=addons) is False:
            print("Failed to connect to Deepgram")
            return

        stream = sd.InputStream(callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, loop), dtype='int16', channels=1, samplerate=16000)
        stream.start()

        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        finally:
            stream.stop()
            stream.close()
            await dg_connection.finish()
        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

async def shutdown(signal, loop, dg_connection, stream):
    print(f"Received exit signal {signal.name}...")
    stream.stop()
    stream.close()
    await dg_connection.finish()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Shutdown complete.")




# Ensure STT only starts when called explicitly
if __name__ == "__main__":
    print("Starting the speech-to-text service...")
    asyncio.run(speech_to_text())
    print("Service stopped.")

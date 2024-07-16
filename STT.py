

from config import API_KEY, TEXT_FILE
from signal import SIGINT, SIGTERM
import asyncio
import sounddevice as sd
import logging
from deepgram import (
    DeepgramClientOptions,
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

logging.basicConfig(level=logging.INFO)
is_finals = []
wait_for_activation = asyncio.Event()

async def speech_to_text():  # method to convert speech to text
    global is_finals
    is_finals = []

    try:
        loop = asyncio.get_event_loop()

        for signal in (SIGTERM, SIGINT):  # handle signals
            loop.add_signal_handler(
                signal,
                lambda: asyncio.create_task(
                    shutdown(signal, loop, dg_connection, stream)
                ),
            )

        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram = DeepgramClient(API_KEY, config)
        dg_connection = deepgram.listen.asynclive.v("1")


        async def send_to_deepgram(data):  # method to send audio data to Deepgram
            await wait_for_activation.wait()  # wait for activation signal
            await dg_connection.send(data)


        def audio_callback(indata, frames, time, status, loop):  # method to handle audio data
            if status:
                logging.warning(status)
            # asyncio.run_coroutine_threadsafe(send_to_deepgram(indata.tobytes()), loop=loop)
            asyncio.run_coroutine_threadsafe(send_to_deepgram(indata.tobytes()), loop)



        async def on_open(self, open, **kwargs):  # method to handle connection open
            logging.info(f"Connection Open")



        async def on_message(self, result, **kwargs):  # method to handle messages
            global is_finals
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:  # check if the sentence is empty
                return
            if result.is_final:  # check if the result is final
                is_finals.append(sentence)
                logging.info(f"Speech Final: {sentence}")
            else:
                logging.info(f"Interim Results: {sentence}")



        async def on_metadata(self, metadata, **kwargs):  # method to handle metadata
            logging.info(f"Metadata: {metadata}")



        async def on_speech_started(self, speech_started, **kwargs):  # method to handle speech start
            logging.info(f"Speech Started")
            with open(TEXT_FILE, "a") as final_text_file:
                pass  # Ensure the file is opened and ready for appending



        async def on_utterance_end(self, utterance_end, **kwargs):  # method to handle utterance end
            logging.info(f"Utterance End")
            utterance = " ".join(is_finals)
            # with open(TEXT_FILE, "a") as final_text_file:
               # final_text_file.write(utterance + "\n")
            await shutdown(SIGINT, loop, dg_connection, stream)



        async def on_close(self, close, **kwargs):  # method to handle connection close
            logging.info(f"Connection Closed")



        async def on_error(self, error, **kwargs):  # method to handle errors
            logging.error(f"Handled Error: {error}")



        async def on_unhandled(self, unhandled, **kwargs):  # method to handle unhandled messages
            logging.warning(f"Unhandled Websocket Message: {unhandled}")



        dg_connection.on(LiveTranscriptionEvents.Open, on_open)  # set the event handlers
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)



        options = LiveOptions(  # Set the options for the connection
            model="nova-2",
            language="en-US",
            smart_format=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            interim_results=True,
            utterance_end_ms="1500",
            vad_events=True,
            endpointing=300,
            replace={"mail": "male"},
        )

        addons = {
            #"no_delay": "true"
        }



        logging.info("\n\nStart talking! Press Ctrl+C to stop...\n")
        #if await dg_connection.start(options, addons=addons) is False:  # start the connection
        if await dg_connection.start(options) is False:
            logging.error("Failed to connect to Deepgram")
            return


        stream = sd.InputStream(callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, loop), dtype='int16', channels=1, samplerate=16000)
        # stream.start()

        stream.start()

        try:
            while True:  # keep the connection open
                await asyncio.sleep(1)

        except asyncio.CancelledError:  # handle cancellation
            pass

        finally:  # close the connection
            stream.stop()
            stream.close()
            await dg_connection.finish()

        logging.info("Finished")

    except Exception as e:
        logging.error(f"Could not open socket: {e}")
        return



async def shutdown(signal, loop, dg_connection, stream):  # method to shutdown the service
    with open(TEXT_FILE, "a") as final_text_file:
        final_text_file.write(" ".join(is_finals) + "\n")

    logging.info(f"Received exit signal {signal.name}...")
    stream.stop()
    stream.close()
    await dg_connection.finish()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]  # cancel all tasks

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    logging.info("Shutdown complete.")



# Ensure STT only starts when called explicitly
if __name__ == "__main__":
    logging.info("Starting the speech-to-text service...")
    asyncio.run(speech_to_text())
    logging.info("Service stopped.")








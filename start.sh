rasa train;
rasa run actions --cors "*" &
rasa run --enable-api --cors "*" &
python service/processor.py

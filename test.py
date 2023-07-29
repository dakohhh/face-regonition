import pickle



with open("model.pkl", "rb") as f:
    encoded_model = pickle.load(f)



for _ in encoded_model:
    print(_.firstname)
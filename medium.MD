
The model.fit() interface provided by Tensorflow and Keras is simple and easy to use; pass in some NumPy vectors, callbacks, and various parameters and you’re set:

  

```python

import tensorflow as tf

model = tf.keras.Model(inputs=inputs, outputs=outputs)

  

early_stopping = tf.compat.v1.keras.callbacks.EarlyStopping(monitor="val_loss", mode="min", verbose=1, patience=5)
model.fit(x=X_train, y=y_train, validation_data=(X_val, y_val), epochs=10, callbacks = [early_stopping])

  ```
model.fit() can prove to be quite limiting. This becomes apparent when training on datasets that become so large that you can no longer fit your whole training set in memory at once. All of a sudden you need a structure that can pipe your dataset into memory chunks at a time to enable continuous training. That’s where tf.keras.model.fit_generator() comes in. It allows you to use keras’ ImageDataGenerator to pull images from a target directory and augment+serialize a batch dataset on the spot. For a code example, see [Tensorflow’s API documentation.](https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/ImageDataGenerator)

  

This is a valid solution to the issue of having datasets too big for memory, but It is slow. VERY slow. Why? Well, on the nth epoch, each training sample needs to be augmented and serialized into NumPy arrays for the nth time. This isn’t something that can be brushed over - it becomes a huge bottleneck and can skyrocket the training time for each epoch. Here is a crude formula for total training time:

 ```
Let x = dataset_read_time+serialization_time+augmentation_time
training_time = (epoch_training time+x)*num_epochs
```
  
If we augment and serialize our dataset, then write that to memory before training even starts, substituting our formula becomes:
```
training_time = x + (epoch_training time + dataset_read_time) * num_epochs
```
Essentially, the longer (more epochs) we train for, the more this serialization bottleneck becomes amortized (we save x*num_epochs - dataset_read_time). Let’s say for example:

```
serialization_time = 4 hours
augmentation_time = 2 hours
dataset_read_time = 1 hour
epoch_training_time = 1.5 hours
num_epochs = 15
x = 7 hours
```
  
These values are in the ballpark of what I’ve observed from my experience when training datasets with several hundred thousand images. Read time will greatly depend on the size of your image files.

With ImageDataGenerator,
```
training_time = (1.5+7)*15 = 127.5 hours (over 5 days!)
```
With our hypothetical setup where we have everything ready to feed into the model,
```
training_time = 7 + (1.5+1)*15 = 44.5 hours (around ⅓ of the time!)
```
  
Note this is being generous to Tensorflow, assuming that it will be as efficient as us at serializating and preparing the dataset. From my experience, it will take at least twice as long:
```
training_time = 2*(1.5+7)*15 = 255 hours
```
  
It’s not over yet though. This 6x difference really shines when you realize that hyperparameter tuning is still necessary. 

To get around this, we can serialize into numpy arrays beforehand, generate several pickle files, and load these files in batches at a time. A custom generator for a dataset of text and images would look something like: 
```python
import  concurrent

import random

  

start = 0

def serial_generator(self, directory, batch_size, file_count, use_mp=True):

	pkl_files = getListOfFiles(directory)

	random.shuffle(pkl_files)

	total = len(pkl_files)

	print(f"processing {total} files for this epoch")

	prog = 0

	for  meganum  in  range(0, total, file_count):

		grab_files = min(meganum + file_count, total)

		if  use_mp:

			start = time.time()

			megabatches = read_parallel(pkl_files[meganum:grab_files])

	else:

		megabatches = pkl_files[meganum:grab_files]

		for  megabatch  in  megabatches:

			if  not  use_mp:

				megabatch = self.open_image(megabatch)

			images = megabatch["images"]

			labels = megabatch["labels"]

			texts = megabatch["texts"]

			megabatch_size = labels.shape[0]

			for  start  in  range(0, megabatch_size, batch_size):

				end = min(start + batch_size, megabatch_size)

				imgs = images[start:end, :, :, :]

				lbls = labels[start:end]

				txts = texts[start:end]

				prog += end - start

				print(f"{prog} -- max_val: {self.max_validation} -- last_val: {self.validation_scores[-1]}")

				yield  txts, imgs, lbls

			del  megabatches, megabatch, images, labels, texts

			print(f"files took {time.time()-self.start} seconds")

  
  

def read_parallel(self, file_names):

	with  concurrent.futures.ThreadPoolExecutor() as  executor:

	futures = [executor.submit(self.open_image, f) for  f  in  file_names]

	return [fut.result() for  fut  in  futures

  ```
  
This code load file_count number of pkl_files from the target directory at a time using parallel reads for each pkl file.

How can we use this generator in our training? Note that we are keeping the validation set stored in memory (it doesn’t need to be that proportionally big on datasets of this scale).
```python

def custom_model_check(self):

	if  self.validation_scores[-1] > self.max_validation:

	self.max_validation = self.validation_scores[-1]

	return  True

  
import joblib

for  epoch  in  range(EPOCHS):

	train_generator = serial_generator(train_dir, BATCH_SIZE, 6)

	train_acc = 0

	while  True:

		try:

			txts, imgs, lbls = next(train_generator)

			x = [txts, imgs]

			y = lbls

			hist = model.train_on_batch(

			x=x, y=y, reset_metrics=False, class_weight=class_weight

			)

			train_acc = hist[1]

			print(f"loss: {hist[0]} --- train_acc: {hist[1]}")

		except  StopIteration:

			print("epoch finished")

			self.training_scores.append(train_acc)

			break

		total_val = 0

		val_acc = 0

		for  set  in  validation_sets:

			total_val += set["labels"].shape[0]

		for  set  in  validation_sets:

			X_val = [set["texts"], set["images"]]

			y_val = set["labels"]

			_, val_acc_mini = model.evaluate(X_val, y_val, batch_size=32)

			print(val_acc_mini)

			val_acc += val_acc_mini * (y_val.shape[0] / total_val)

		print(f"val_acc for epoch {epoch}: {val_acc}")

		self.validation_scores.append(val_acc)

		if  custom_model_check():

			g = "{:.2f}".format(val_acc)

			model_name = os.path.join(

			"models", f"model.h5"

			)

			print(f"saving model {model_name}...")

			model.save_weights(model_name)

			early_stopping = 5

		else:

			early_stopping -= 1

			print(f"val_acc did not improve from {self.max_validation}")

			if  not  early_stopping:

			print(f"Early stopping at epoch {epoch}")

			break

	joblib.dump(

	{"train": self.training_scores, "val": self.validation_scores}, ftraining_results.pkl"

	)

  ```

  

As you can see, the generator exhausts its supply of data containing pickle files, loaded in batch by batch into memory per epoch. It is up to you on how you want to serialize your dataset, but this gives a demonstration on how to write your own custom generator and make use of it using the train_on_batch interface.

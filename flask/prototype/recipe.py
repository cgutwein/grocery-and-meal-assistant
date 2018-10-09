from shutil import copyfile
from flask import Flask, render_template, request
from werkzeug import secure_filename
import tablib
import os

app = Flask(__name__, instance_relative_config=True)

def mycopy(fname):
   copyfile(fname, 'new_file.csv')
   dataset = tablib.Dataset()
   with open('new_file.csv') as f:
      dataset.csv = f.read()
   return dataset.html

@app.route('/home')
def home():
   return render_template('index.html')
	
@app.route('/results', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      radio_selection = request.form['user_options']
      list_selection = request.form['city']
      f = request.files['file']
      f.save(secure_filename(f.filename))
      result_page = mycopy(f.filename)
      return result_page
		
if __name__ == '__main__':
   app.run()
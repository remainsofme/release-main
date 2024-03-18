from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash
import functions
import json
import os


app=Flask(__name__)
app.secret_key='hello'
upload_folder='/static/image'
app.config['UPLOAD_FOLDER']=upload_folder

@app.route('/')
def index():
    return redirect('/gallery_maker')

@app.route('/gallery_maker',methods=['POST','GET'])
def gallery_maker():
    content_type=request.headers.get('Content-Type')
    if request.method=='GET':
        if 'pdfs' not in os.listdir('static'):
            os.mkdir('static/pdfs')
        if 'result.pdf' in os.listdir('static/pdfs'):
             os.remove('static/pdfs/result.pdf')
        
        if 'image' not in os.listdir('static'):
            os.mkdir('static/image')
        for file in os.listdir('static/image'):
            os.remove('static/image'+'/'+file)
        return render_template('gallery_maker.html')
    if request.method=='POST':  
        if content_type=='application/json':
            filled_table=request.get_json()
            functions.parse_pdf(filled_table)
            
            response_data={'message':'successfully received'}
            return jsonify(response_data)
        else:
            files=request.files.getlist('my_files')
            if not files:
                flash('No file in request')
                response_data={'message':'not received'}
                return jsonify(response_data)
            else:
                for file in files:
                    if file:
                        file.save('static/image/'+file.filename)
                refresh_data=jsonify(functions.table())    
                return refresh_data
            
@app.route('/personal_information_form',methods=['GET','POST'])     
def personal_info():
    if request.method=='GET':
        return render_template('personal_info_form.html')    
    if request.method=='POST':
        print(request.form)
        return redirect(url_for('profession_form'))    

@app.route('/profession_form',methods=['GET','POST'])     
def profession_form():
    if request.method=='GET':
        return render_template('profession_form.html')    
    if request.method=='POST':
        print(request.form)
        return redirect(url_for('related_person'))
    
@app.route('/related_person',methods=['GET','POST'])     
def related_person():
    if request.method=='GET':
        return render_template('related_person.html')    
    if request.method=='POST':
        print(request.form)
        return render_template('related_person.html') 
    

if __name__=='__main__':
    app.run()
    
    

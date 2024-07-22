from flask import Flask,render_template,request
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import re
import os
os.environ["OPENAI_API_KEY"]="secret key"

app=Flask(__name__)

llm_resto=OpenAI(temperature=0.6)
prompt_template_resto = PromptTemplate(
    input_variables=['age','gender','weight','height','veg_or_nonveg','disease','region','foodtype','city'],
    template="Diet Recommendation System:\n"
        "I want you to  recommend 6 restaurants names of {city} , 6 breakfast names , 6 dinner names , 6 workout names ,"
        "based on the following criteria:\n"
        "Person age:{age}\n"
        "Person gender:{gender}\n"
        "Person weight:{weight}\n"
        "Person height:{height}\n"
        "Person veg_or_nonveg:{veg_or_nonveg}\n"
        "Person disease:{disease}\n"
        "Person region:{region}\n"
        "Person foodtype:{foodtype}\n"
        'city:{city}\n'
)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/recommend' , methods=['POST'])

def recommend():
    if request.method=='POST':
        age=request.form['age']
        gender=request.form['gender']
        weight=request.form['weight']
        height=request.form['height']
        veg_or_nonveg=request.form['veg_or_nonveg']
        disease=request.form['disease']
        region=request.form['region']
        foodtype=request.form['foodtype']
        city=request.form['city']

        chain_resto=LLMChain(llm=llm_resto,prompt=prompt_template_resto)
        input_data={
            'age':age,
            'gender':gender,
            'weight':weight,
            'height':height,
            'veg_or_nonveg':veg_or_nonveg,
            'disease':disease,
            'region':region,
            'foodtype':foodtype,
            'city':city
    }
        result=chain_resto.run(input_data)

    
        resto_name=re.findall(r'Restaurants:(.*?)Breakfast:',result,re.DOTALL)
        Breakfast_name=re.findall(r'Breakfast:(.*?)Dinner:',result,re.DOTALL)
        Dinner_name=re.findall(r'Dinner:(.*?)Workouts:',result,re.DOTALL)
        Workouts_name=re.findall(r'Workouts:(.*?)$',result,re.DOTALL)

        resto_name=[name.strip() for name in resto_name[0].strip().split('\n') if name.strip()] if resto_name else []
        Breakfast_name=[name.strip() for name in Breakfast_name[0].strip().split('\n') if name.strip()] if Breakfast_name else []
        Dinner_name=[name.strip() for name in Dinner_name[0].strip().split('\n') if name.strip()] if Dinner_name else []
        Workouts_name=[name.strip() for name in Workouts_name[0].strip().split('\n') if name.strip()] if Workouts_name else []
        
        return render_template('result.html',resto_name=resto_name,  Breakfast_name= Breakfast_name, Dinner_name=Dinner_name ,Workouts_name=Workouts_name  )
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
# import mysql.connector
import re
import string
import random
import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import redirect


def home(request):
    return render(request, 'home.html')


def hereIsYourRatting(user_password):
    answer = 5
    if len(user_password) < 8:
        answer = answer - 1

    if not re.search("[a-z]", user_password) or not re.search("[A-Z]", user_password):
        answer = answer - 1

    if not re.search("[0-9]",user_password):
        answer = answer - 1

    if not re.search("[!@#$%^&*()_+=\-[\]{};':\"|,.<>/?]", user_password):
        answer = answer - 1
    return answer

def get_password(request):
    if request.method == 'POST':
        context = {}
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sai@121530",
            database="secure_password_application"
        )

        query = "SELECT * FROM sairaj_adding_password"
        df = pd.read_sql(query,con=mydb)
        mycursor = mydb.cursor()
        website = request.POST.get('h11')
        user_name = request.POST.get('h12')
        intrest_data = df[df['website_name'] == website]
        context = df.to_dict()

        context_json = json.dumps(context)
        print(context_json)
        return render(request,'retrieve_data.html',{'context_json': context_json})
    return HttpResponse("hey")

def giveMeNewPassword():
    # Define the characters to use for the password
    characters = string.ascii_letters + string.digits + string.punctuation
    length = len(characters)
    # Generate a password by randomly selecting characters
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

    # Example usage

def add_password(request):
    if request.method == 'POST':
        context = {}
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sai@121530",
            database="secure_password_application"
        )
        mycursor = mydb.cursor()
        website = request.POST.get('h1')
        user_name = request.POST.get('h2')
        user_password = request.POST.get('h3')
        if len(user_password) == 0:
            user_password = giveMeNewPassword()

        rating = hereIsYourRatting(user_password)
        # rating = 5
        print(website,user_name,user_password)
        sql_query = "SELECT id FROM sairaj_adding_password ORDER BY id DESC LIMIT 1"
        mycursor.execute(sql_query)

        result = mycursor.fetchone()
        #print(result[0])
        if result is None:
            print("Yes it is none type")
            id = 0
        else:
            print("NO not")
            id = result[0] + 1

        sql = "INSERT INTO sairaj_adding_password (website_name, user_account, user_password, ratting,id) VALUES (%s, %s, %s, %s,%s)"
        values = (website, user_name, user_password, rating,id)

        mycursor.execute(sql, values)
        mydb.commit()
        context = {'responded' : 'yes response is recieved'}
        print(context)
        return redirect('add_password')
    return HttpResponse("data added succesfully")

def change_password(request):
    if request.method == 'POST':
        context = {}
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sai@121530",
            database="secure_password_application"
        )
        mycursor = mydb.cursor()
        user_request = request.POST.get('h11')
        query = "SELECT * FROM sairaj_adding_password"
        df = pd.read_sql(query, con=mydb)
        intrest_data = df[df['website_name'] == user_request]
        if len(intrest_data) == 0:
            return HttpResponse("please enter the website name correctly")

        context = df.to_dict()
        context_json = json.dumps(context)
        return render(request,'user_data.html',{'context_data':context_json})
    return HttpResponse("Be the giga chad")


def user_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        index = data.get('index1')
        print(index)
        user_name = data.get('newName')
        user_password = data.get('newPassword')

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sai@121530",
            database="secure_password_application"
        )

        mycursor = mydb.cursor()

        # Update the column values for a specific condition using the id column
        sql_update = """
        UPDATE sairaj_adding_password
        SET user_account = %s, user_password = %s, ratting = %s
        WHERE id = %s
        """

        rating = hereIsYourRatting(user_password)
        values = (user_name, user_password, rating, index)
        mycursor.execute(sql_update, values)
        mydb.commit()

        print(user_password)

        mycursor.close()
        mydb.close()

        return JsonResponse({"message": "Data received successfully"})

    return JsonResponse({'message': 'Gigachad'})


def coder_kira_12(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        index = data.get('index1')
        print(index)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sai@121530",
            database="secure_password_application"
        )

        mycursor = mydb.cursor()
        query = "DELETE FROM sairaj_adding_password WHERE id = %s"
        mycursor.execute(query, (index,))
        print("my value is ", index)

        # Get the number of rows affected by the delete operation
        rows_affected = mycursor.rowcount

        # Commit the changes to the database
        mydb.commit()

        # Close the database connection
        mycursor.close()
        mydb.close()

        if rows_affected > 0:
            return JsonResponse({"done": f"{rows_affected} row(s) deleted"})
        else:
            return JsonResponse({"done": "No rows deleted"})

    return HttpResponse("Bokuga kirada")

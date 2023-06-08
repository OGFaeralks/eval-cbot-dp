import csv
import time
import requests

queries = [
    "I have had a runny nose and have been coughing and have had on and off headaches. I went to the doctor the first time, he gave me an antibiotic and i got worse then I went back a and he gave me a different one but it seems I still have these symptoms?",
    "I've been in contact with a possible covid-19 case who is waiting on results. My brother seems to be I'll with Corona symptoms and I'd like to get advice on how to help him, as his safety will ensure my safety and prevent the spread of the virus.",
    "I travelled to Mauritius and do not have symptoms. Should I get tested for covid19?",
    "What symptoms would make you think I do not have COVID-19. I have a bad cold, but got diarrhea twice, so does diarrhea mean it is not COVID?",
    "Can Covid-19 be transmitted sexually? Can any coronavirus be transmitted sexually?",
    "Have read COVID-19 news quoting some experts as saying that we will see more confirmed cases as more tests are performed, but the mortality rate should drop as that happens. Any sign of that yet?",
    "I travelled to Austria on 25 Jan 2020 and returned on 31Jan 2020. My trip included a stopover in Munich. I currently do not show any symptoms listed for coronavirus. Should i get lab tested as a precaution and will this test be covered by the medical?"
    "For students in dorms living with students from many countries, what extra additional precautions do they need to prevent catching novel coronavirus?",
    "Can taking extra vitamin C every day help prevent you from catching the coronavirus or the flu? If so, how much vitamin C is recommended?",
    "Can taking extra steps for self-care (like staying hydrated, getting more sleep) every day help prevent you from catching the coronavirus or the flu?",
    "Last tuesday I had a flu shot and a neumonia shot. I am 68 and male. I had a very sore arm and felt bad the next day in which I had blood drawn for a test. The results showed a high white cell blood count as well as high ANC and AMC. Could these high readings be because of the shots the day before?",
    "My father recently passed over the weekend. His body was fighting an infection along with pneumonia for 1 week. During that time, he would urinate bloody urine into the foley. The doctors said that was completely normal. It was very dark red. Is that normal?",
    "I have pneumonia and my doctor has me on strong antibodics and albut in my nebulizer. Yesterday after a treatment I spit up fresh blood and I have this second day also. I m on blood thinners and wonder if that may be my problem. I feel better in other ways.",
    "Hi, my name is XXXX. My grandfather is suffering from pneumonia right now and refuses to go to the doctor because of the price needed to obtain a patented medicine. In Indonesia, it is not hard to find these kinds of doctors that don t want to help people in need. What medicine can you guys recommend for a home treatment?",
    "I was diagnosed with pneumonia on june 30. I finished taking my antibiotics and cough pills. I still continue to cough sometimes gaging. Shortness of breath and wheezing, I have an inhaler, I am not coughing up anymore phlem. my doctor says to take Mucinex DM. I have finished a bottle. I also have taken robitussin cough medicine. She also sd cough cld last up to 4-6 weeks.",
    "Hi my husband has been diagnosed with pneumonia and given roxithromycin, he s had a heart transplant 4 yrs ago he is very tired hardly eating or drinking pretty larthargic to be honest should I be taking him to hospital we are now on day 3 on the antibiotics with no improvement what would you suggest?"
]

def getTime(message):
    ave_time = 0
    highest_time = 0

    for i in range(10):
        # Set the URL of your Rasa server
        rasa_server_url = 'http://localhost:5005/webhooks/rest/webhook'

        # Make a POST request to the Rasa server and measure the response time
        start_time = time.time()
        response = requests.post(rasa_server_url, json={"message": message})
        end_time = time.time()

        # Extract the response content
        response_content = response.json()

        # Calculate the response time in milliseconds
        response_time_ms = (end_time - start_time) * 1000

        # Print the response and response time
        print("Response:")
        print(response_content)
        ave_time += response_time_ms
        if response_time_ms > highest_time:
            highest_time = response_time_ms
        # print("Response time: {:.2f} ms".format(response_time_ms))

    # print(f"For the text: {message}")
    # print("Average time in 10 attempts: {:.2f} ms".format(ave_time / 10))
    # print("Highest time: {:.2f} ms".format(highest_time))
    
    return [len(message), ave_time / 10, highest_time]

# Create a CSV file
csv_file = open("response_times.csv", "w", newline="")
csv_writer = csv.writer(csv_file)

# Write the header row in the CSV file
csv_writer.writerow(["Query Size", "Average Time (ms)", "Highest Time (ms)"])

# Iterate over the queries
for query in queries:
    response_times = getTime(query)
    
    # Write the response times to the CSV file
    csv_writer.writerow(response_times)

# Close the CSV file
csv_file.close()
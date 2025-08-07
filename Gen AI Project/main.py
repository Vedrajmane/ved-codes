import groq
from groq import Groq
import customtkinter
from PIL import Image
import unicodedata

client = Groq(
    api_key="Your API key",
)


def chat(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        model="llama3-groq-70b-8192-tool-use-preview",
    )

    return chat_completion


# ____________________________________UI________________________________________

def submit():

    try:
        prompt1 = f"""Generate a detailed nutrition Table report for the following food item and quantity :

                    Food Item: {food_entry.get()}
                    Quantity: {food_entry2.get()} 
                    
                    Please provide the report in the following format in 20 rows:
                    
                    Nutrient Contains : Measurement (Unit) : % of Daily Requirement
                    
                    for ex.
                    
                    
                    (give a proper spacing so above format looks like a table)
                    for ex.
                    Nutrient Contains  |   Measurement (Unit)    |    % of Daily Requirement
                    Protein                  4gm                        1%
                    fat                      3gm                        2%
                    
                        
                    

                    Please use reliable sources, such as the United States Department of Agriculture (USDA) or the National Nutrient Database, to ensure accuracy.
                    -Don't add the symbols like **,## ~ in the generated text 
                    -Dont generate any note or suggestion at the last text than given format
                    """

        prompt2 = f"""  Provide personalized nutrition and health suggestions based on the following food item and quantity:
        
                      
                        Food Item: {food_entry.get()}
                        Quantity: {food_entry2.get()}
                        
                        Assume my goals are:
                        
                        -{food_entry3.get("0.0","end")}
                        
                        
                        Format your suggestions as a personalized consultation in 200 words max(point wise), (goal : {food_entry3.get("0.0", "end")})
                    
                            
                        

                        Use evidence-based information and reliable sources, such as the Academy of Nutrition and Dietetics or the World Health Organization, to support your suggestions.
                        
                        remind before generating,
                        -Give Titles in this format ex | Title |,
                        -point wise
                        -length : 10 lines(max),
                        -Don't generate the symbols like **,## ~ or non alphanumeric characters in the text for formatting,
                        -generate a plain text for better understanding,
                        -only generate - for each point, allign lines form left side,
                        -Dont generate any other text than given format,
                        -length of line : max 8 words
                        
                    """
        stat_window = customtkinter.CTk()
        stat_window.geometry("1024x600")
        stat_window.title("Statistics")
        stat_window.resizable(width=False, height=False)

        stat_view = customtkinter.CTkTabview(master=stat_window, width=200, border_width=2, border_color="grey")
        stat_view.pack(padx=20, pady=20)

        stat_view.add("Gained Nutrients")
        stat_view.add("Suggestions")

        label = customtkinter.CTkLabel(master=stat_view.tab("Gained Nutrients"), text=unicodedata.normalize("NFKD",chat(prompt1).choices[0].message.content).encode("ascii","ignore").decode("utf-8"), font=("Poppins", 15, "normal"))
        label.grid(row=0, column=0, padx=20, pady=10)

        label = customtkinter.CTkLabel(master=stat_view.tab("Suggestions"), text=unicodedata.normalize("NFKD",chat(prompt2).choices[0].message.content).encode("ascii", "ignore").decode("utf-8"), font=("Poppins", 15, "normal"))
        label.grid(row=0, column=0, padx=20, pady=10)

        stat_window.mainloop()
    except (ConnectionError, groq.APIConnectionError):
        error = customtkinter.CTkToplevel(window)
        error.title("Network Error")
        error.attributes('-topmost', True)
        msg = customtkinter.CTkLabel(master=error, text="Check Internet Connection", font=("verdana", 15, "normal"))
        msg.pack(padx=20, pady=20)


window = customtkinter.CTk()
window.title("Diet Consultant")
window.geometry("1024x600")
window.resizable(width=False, height=False)
window.configure(fg_color="#FBBA00")

# Banner
banner_frame = customtkinter.CTkFrame(window, width=1024, height=150, border_color="black", border_width=0)
banner_frame.grid(column=0, row=0, sticky="nsew")

banner = customtkinter.CTkImage(light_image=Image.open("banner.jpg"), size=(1024, 150))
banner_image = customtkinter.CTkLabel(master=banner_frame, image=banner, text="")
banner_image.grid(column=0, row=0)

# body

body_Frame = customtkinter.CTkFrame(window, height=450, border_color="black", border_width=3, corner_radius=20)
body_Frame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

# Food Entry
food_entry_Frame = customtkinter.CTkFrame(body_Frame, border_color="black", border_width=1, corner_radius=20)
food_entry_Frame.grid(column=0, row=0, padx=20, pady=20, sticky="nw")

recipie_label = customtkinter.CTkLabel(master=food_entry_Frame, text="Recipie/Food", font=("Kanit", 20, "bold"))
recipie_label.grid(column=0, row=0, padx=5, pady=5)

food_entry = customtkinter.CTkEntry(master=food_entry_Frame, placeholder_text="Enter Food/Recipie", width=400, height=40)
food_entry.grid(column=0, row=1, padx=30, pady=20)


# Quantity
food_entry_Frame = customtkinter.CTkFrame(body_Frame, border_color="black", border_width=1, corner_radius=20)
food_entry_Frame.grid(column=1, row=0, padx=10, pady=20, sticky="nw")

quantity_label = customtkinter.CTkLabel(master=food_entry_Frame, text="Quantity", font=("Kanit", 20, "bold"))
quantity_label.grid(column=0, row=0, padx=5, pady=5)

food_entry2 = customtkinter.CTkEntry(food_entry_Frame, placeholder_text="Enter Quantity", width=400, height=40)
food_entry2.grid(column=0, row=1, padx=30, pady=20)


# Describe Food
food_description_Frame = customtkinter.CTkFrame(body_Frame, border_color="black", border_width=1, corner_radius=20)
food_description_Frame.grid(column=0, row=1, padx=20, pady=5, sticky="nw", columnspan=2)

description_label = customtkinter.CTkLabel(master=food_description_Frame, text="Health Goals", font=("Kanit", 20, "bold"))
description_label.grid(column=0, row=0, padx=5, pady=10)

food_entry3 = customtkinter.CTkTextbox(master=food_description_Frame, width=940, height=100, corner_radius=20, border_width=2, border_color="black")
food_entry3.grid(column=0, row=1, padx=10, pady=20)

quantity = food_entry2.get()
entry = food_entry.get()
description = food_entry3.get("0.0", "end")

# Button

button = customtkinter.CTkButton(master=body_Frame, corner_radius=30, border_color="black",border_width=1, text="Submit", font=("Kanit",15,"bold" ), text_color="white", width=200, height=40,fg_color="#047652", hover_color="#FBBA00", command=submit)
button.grid(column=0, row=2, columnspan=2, pady=15)


window.mainloop()

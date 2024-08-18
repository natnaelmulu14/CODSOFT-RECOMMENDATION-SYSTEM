import pandas as pd
from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame

movies = pd.read_csv(r'E:\programming\Spacy\Movie recommender\MoviesOnStreamingPlatforms_updated.csv')
movies.dropna(subset=['Genres', 'Age'], inplace=True)
genres = movies['Genres'].str.split(',').explode().str.strip().unique()

gen_filt = movies.copy()
gen_filt['Genres'] = movies['Genres'].apply(lambda gen: gen.split(','))
gen_filt['Genres'] = gen_filt['Genres'].apply(tuple)
age_filt = movies.copy()
age_filt['Genres'] = movies['Genres'].apply(lambda gen: gen.split(','))
age_filt['Genres'] = age_filt['Genres'].apply(tuple)

def recommender():
    final_filter = pd.merge(gen_filt, age_filt)
    final_filter = final_filter.sort_values(['IMDb'], ascending=False)
    final_list = final_filter[['Title','IMDb','Language', 'Genres']].values.tolist()
    # print(final_filter[['Title','IMDb','Language', 'Genres']])
    display(final_list)
    # print(x['Genres'])
    # print(y[['Age', 'Genres']])

def display(final_list):
    display_tree.delete(*display_tree.get_children())
    for row in final_list:
        display_tree.insert('', END, values=row)

def genre_filter():
    global gen_filt
    gen_filt = movies.copy()
    gen_filt_copy = movies['Genres'].copy()
    gen_filt['Genres'] = movies['Genres'].apply(lambda gen: gen.split(','))
    # print(filtered_movies['Genres'])
    
    movies['Genres'] = movies['Genres'].apply(lambda gen: gen.split(','))
    # print(movies['Genres'])
    for variable in variables:
        for genre, var in variable.items():
            if var.get() == 1:
                filtered = movies[movies['Genres'].apply(lambda row: genre in [gen.strip() for gen in row])]
                filtered['Genres'] = filtered['Genres'].apply(tuple)
                gen_filt['Genres'] = gen_filt['Genres'].apply(tuple)
                gen_filt = pd.merge(gen_filt,filtered)
            else:
                gen_filt['Genres'] = gen_filt['Genres'].apply(tuple)
    movies['Genres'] = gen_filt_copy

    recommender()

def age_filter(e):
    global age_filt
    age_filt = movies.copy()
    age_filt['Genres'] = movies['Genres'].apply(lambda gen: gen.split(','))
    age_filt['Genres'] = age_filt['Genres'].apply(tuple)
    age = age_menu.get()
    age = int(str(age).split('+')[0])
    if age in range(7,13):
        filtered = age_filt[(age_filt['Age'] == 'all') | (age_filt['Age'] == '7+')]
    elif age in range(13, 16):
        filtered = age_filt[(age_filt['Age'] != '18+') & (age_filt['Age'] != '16+')]
    elif age in range(16, 17):
        filtered = age_filt[age_filt['Age'] != '18+']
    else:
        filtered = age_filt
    
    age_filt = filtered
    recommender()

def reset():
    global gen_filt 
    global age_filt
    for variable in variables:
        for genre, var in variable.items():
            var.set(0)
    age_menu.set('')
    gen_filt = movies.copy()
    gen_filt['Genres'] = movies['Genres'].apply(lambda gen: gen.split(','))
    gen_filt['Genres'] = gen_filt['Genres'].apply(tuple)
    age_filt = movies.copy()
    age_filt['Genres'] = movies['Genres'].apply(lambda gen: gen.split(','))
    age_filt['Genres'] = age_filt['Genres'].apply(tuple)
    recommender()


movies = pd.read_csv(r'E:\programming\Spacy\Movie recommender\MoviesOnStreamingPlatforms_updated.csv')
movies.dropna(subset=['Genres', 'Age'], inplace=True)
genres = movies['Genres'].str.split(',').explode().str.strip().unique()
print(len(genres))
root = tb.Window(themename="superhero")
root.title("TTK Bootstrap!")
root.geometry('1200x700')


nav = Frame(root)
nav.pack(pady=20)

main_frame = Frame(root)
main_frame.pack(expand=True, fill=BOTH)

# search_bar = tb.Entry(nav, width=50)
# search_bar.grid(column=0, row=0)
# search_btn = tb.Button(nav, text="Search", bootstyle="outline")
# search_btn.grid(column=1, row=0)

ages = []
for age in range(7,18):
    ages.append(age)
    if age == 17:
        ages.append("18+")
age_label = tb.Label(nav, text="Age:")
age_label.grid(column=1, row=0)

age_menu = tb.Combobox(nav, width=5, values=ages)
age_menu.grid(column=2, row=0, padx=20)
age_menu.bind("<<ComboboxSelected>>", age_filter)

reset_button = tb.Button(nav, text='Reset', command=reset)
reset_button.grid(column=3, row=0, padx=10)

side_frame = ScrolledFrame(main_frame, height=700)
main_frame.grid_columnconfigure(0, weight=1)

side_frame.grid(column=0, row=0, sticky="nw", padx=30, pady=10)

Row = 0
variables = []
for genre in genres:
    var= IntVar()
    variables.append({genre:var})
    tb.Checkbutton(side_frame, text=genre, onvalue=1, offvalue=0, variable=var, command= genre_filter).grid(column=0, row=Row, pady=2, sticky="w", padx=20)
    Row += 1





columns = ("movie_name", "rating_imdb", "language", "genre")

display_tree = tb.Treeview(main_frame, bootstyle="success", columns=columns,
show="headings", height=500)
main_frame.grid_columnconfigure(1, weight=3)
display_tree.grid(column=1, row=0, sticky='nsw')

display_tree.heading('movie_name', text="Movie")
display_tree.heading('rating_imdb', text="Rating IMDB")
display_tree.heading('language', text="Language")
display_tree.heading('genre', text="Genre")



root.mainloop()





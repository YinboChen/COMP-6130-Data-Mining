from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
import threading
import time
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
print (dir_path)
root = Tk()

def click_effectiveness_button():
    if button_left_main_eff.image == button_off_eff:
        #click
        button_left_main_eff.config(image= button_on_eff)
        button_left_main_eff.image = button_on_eff       
        frame_eff.place(x= 220, y= 90)    
        eff_text.place(x=200,y=5)
        eff_number_clients.place(x=40, y=100)
        eff_dataset.place(x=320,y=100)
        eff_learning_rate.place(x=50,y=160)
        eff_alpha.place(x=325,y=160)
        eff_total_epochs.place(x=55,y=220)
        eff_algo.place(x=50, y=280)
        eff_r.place(x=335,y=220)

        #input values for effectiveness frame
        #intial var
        number_clients_var = IntVar()
        dataset_var = StringVar()
        learning_rate_var = DoubleVar()
        alpha_var = DoubleVar()
        epochs_var = IntVar()
        r_var = DoubleVar()
        algo_var = StringVar()
        algo_1_var = StringVar()
        algo_2_var = StringVar()
        algo_3_var = StringVar()
        algo_4_var = StringVar()
        #default settings
        number_clients_var.set(3)
        #dataset_var.set("Mnist")
        learning_rate_var.set(0.01)
        alpha_var.set(0.1)
        epochs_var.set(100)
        r_var.set(0.5)
        #algo_var.set("FedGen")

        eff_running_state = StringVar()
        flag = BooleanVar()
        progressbar_var = IntVar()
        progressbar_pers_var = IntVar()
        avg_glob_accu_var = DoubleVar()
        avg_glob_los_var = DoubleVar()
        file_name = StringVar()

        # animation % vals for frame_eff_1

        

        #built enties for each parameter
        entry_number_clients = Entry(frame_eff,textvariable=number_clients_var,width=10).place(x= 180, y=100)
        dataset_combobox= ttk.Combobox(frame_eff,textvariable=dataset_var,values = ["Mnist","EMnist"],width=10).place(x=390,y=100)
        entry_learning_rate = Entry(frame_eff,textvariable=learning_rate_var,width=10).place(x= 180, y=160)
        entry_alpha = Entry(frame_eff,textvariable=alpha_var,width=10).place(x= 390, y=160)
        entry_total_epochs = Entry(frame_eff,textvariable=epochs_var,width=10).place(x= 180, y=220)
        entry_r = Entry(frame_eff,textvariable=r_var,width=10).place(x= 390, y=220)
        aglo_combobox= ttk.Combobox(frame_eff,textvariable= algo_var,values = ["FedGen","FedAvg","FedProx","FedDistll-FL"],width=10).place(x=180,y=280)
        
        def check_dataset():
            os.chdir(f"/home/yinbo/Desktop/comp6130/final project/final project/FedGen-main/data/{dataset_var.get()}") 
            if os.path.isdir(f"u20c10-alpha{alpha_var.get()}-ratio{r_var.get()}") or os.path.isdir(f"u20-letters-alpha{alpha_var.get()}-ratio{r_var.get()}"):   
                eff_running_state.set(f"Found {dataset_var.get()} Dataset! Press run!")
                flag.set(True)
            else:
                eff_running_state.set(f"Please generate {dataset_var.get()} Dataset!")
                flag.set(False)
                

        #generating child process to execute CLI command
        def generate_or_run_effectiveness_algorithm():
            os.chdir(f"/home/yinbo/Desktop/comp6130/final project/final project/FedGen-main/data/{dataset_var.get()}") 
            if flag.get() ==False:
                eff_running_state.set(f"Generating {dataset_var.get()} Dataset!!!")
                CLI_command_create_data = ["python3", "generate_niid_dirichlet.py", "--n_class", "10","--sampling_ratio", str(r_var.get()), "--alpha", str(alpha_var.get()), "--n_user", "20"]     
                generate_data = subprocess.Popen(CLI_command_create_data)
                generate_data.wait()
                eff_running_state.set(f"Starting {dataset_var.get()} Dataset computing!")          
                os.chdir("/home/yinbo/Desktop/comp6130/final project/final project/FedGen-main/") 
                flag.set(True)
                root.update_idletasks()
            else:
                os.chdir("/home/yinbo/Desktop/comp6130/final project/final project/FedGen-main/") 
                #FedGen, FedAvg,FedProx, and FedDistll-FL
                #cli_command_run_data, currently,it's hard coded, for the testing purpose. 
                #CLI_command_run_data = ["python3", "main.py", "--dataset", str(dataset_var.get()) + "-alpha" + str(alpha_var.get()) + "-ratio" + str(r_var.get()), "--algorithm", "FedAvg", "--batch_size", "32", "--num_glob_iters", "200", "--local_epochs", "20", "--num_users", {number_clients_var.get()}, "--lamda", "1", "--learning_rate", "0.01", "--model", "cnn", "--personal_learning_rate", "0.01", "--times", "1"]
                CLI_command_run_data=["python3", "main.py", "--dataset", str(dataset_var.get()) + "-alpha" + str(alpha_var.get()) + 
                        "-ratio" + str(r_var.get()), "--algorithm", str(algo_var.get()), "--batch_size", "32", "--num_glob_iters", str(epochs_var.get()), \
                        "--local_epochs", "20", "--num_users", str(number_clients_var.get()), "--lamda", "1", "--learning_rate", str(learning_rate_var.get()), \
                        "--model", "cnn", "--personal_learning_rate", "0.01", "--times", "1"]
                print(CLI_command_run_data)
                #subprocess.run()
                run_data = subprocess.Popen(CLI_command_run_data,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                #progressbar persantage% =  count/num_glob_iters* times* 100
                eff_running_state.set(f"Starting {dataset_var.get()} Dataset computing!") 
                count = 0
                os.chdir("/home/yinbo/Desktop/comp6130/final project/final project/txt_results") 
                file_name.set(f"{dataset_var.get()}-alpha{alpha_var.get()}-ratio{r_var.get()}{str(algo_var.get())}-batch_size32-num_glob_iters{epochs_var.get()}--num_users10--learning_rate{learning_rate_var.get()}.txt")
                file= open(file_name.get(),'w')
                #here has an issue, if childprocess exits, there is not read-line...
                while run_data.poll() is None:
                    time.sleep(0.01)  
                    root.update_idletasks()     
                    info = run_data.stdout.readline().decode("utf-8", "ignore")
                    file.write(info)
                    round = '-Round number:'
                    global_line = 'Average Global Accurancy'
                    if re.search(round,info):
                        count = count+1   
                        progressbar_var.set(count)  
                        progressbar_pers_var.set(str(count* (epochs_var.get())/(epochs_var.get()))+"%")
                        #print (count)
                    elif re.search(global_line,info):
                        z = re.findall(r'\d+.\d+',info)
                        avg_glob_accu_var.set(z[0])
                        avg_glob_los_var.set(z[1])
                    #root.update()   
                    #print (run_data.stdout.read())
                eff_running_state.set("Finished computing!")  
                file.close()
                #no...dont do it, cant manually set to 100%...
                #progressbar_pers_var.set("100%") 
                # tips, tips_err = run_data.communicate()
                # print (tips_err)
        def plot_result():
            frame_eff.place_forget()
            frame_eff_1.place_forget()
            frame_eff_2.place(x= 220, y= 90)
            eff_text_2.place(x=200,y=5)

            #built enties for each parameter
            entry_number_clients = Entry(frame_eff,textvariable=number_clients_var,width=10).place(x= 180, y=100)
            dataset_combobox= ttk.Combobox(frame_eff,textvariable=dataset_var,values = ["Mnist","EMnist"],width=10).place(x=390,y=100)
            #entry_learning_rate = Entry(frame_eff,textvariable=learning_rate_var,width=10).place(x= 180, y=160)
            entry_alpha = Entry(frame_eff,textvariable=alpha_var,width=10).place(x= 390, y=160)
            entry_total_epochs = Entry(frame_eff,textvariable=epochs_var,width=10).place(x= 180, y=220)
            entry_r = Entry(frame_eff,textvariable=r_var,width=10).place(x= 390, y=220)
            aglo1_combobox= ttk.Combobox(frame_eff_2,textvariable= algo_1_var,values = ["FedGen","FedAvg","FedProx","FedDistll-FL"],width=10).place(x=50,y=100)
            aglo1_combobox= ttk.Combobox(frame_eff_2,textvariable= algo_2_var,values = ["FedGen","FedAvg","FedProx","FedDistll-FL"],width=10).place(x=175,y=100)
            aglo1_combobox= ttk.Combobox(frame_eff_2,textvariable= algo_3_var,values = ["FedGen","FedAvg","FedProx","FedDistll-FL"],width=10).place(x=300,y=100)
            aglo1_combobox= ttk.Combobox(frame_eff_2,textvariable= algo_4_var,values = ["FedGen","FedAvg","FedProx","FedDistll-FL"],width=10).place(x=425,y=100)

            Label(frame_eff_2,text="Number of Clients",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            Label(frame_eff_2,text="Dataset",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            #Label(frame_eff_2,text="Learning Rate",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            Label(frame_eff_2,text="Alpha",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            Label(frame_eff_2,text="R",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            Label(frame_eff_2,text="Total Epochs",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place()
            Label(frame_eff_2,text="Algorithm 1",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=50, y=70)
            Label(frame_eff_2,text="Algorithm 2",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=175, y=70)
            Label(frame_eff_2,text="Algorithm 3",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=300, y=70)
            Label(frame_eff_2,text="Algorithm 4",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=425, y=70)
            

        def open_file():
            os.chdir("/home/yinbo/Desktop/comp6130/final project/final project/txt_results") 
            os.system("nano "+ file_name.get())
            
        def back_page():
            eff_submit_button.configure(image=button_off_sub)
            eff_submit_button.image = button_off_sub
            avg_glob_accu_var.set(0.0)
            avg_glob_los_var.set(0.0)
            progressbar_pers_var.set(0)
            progressbar_var.set(0)

            number_clients_var.set(3)
            #dataset_var.set("Mnist")
            learning_rate_var.set(0.01)
            alpha_var.set(0.1)
            epochs_var.set(100)
            r_var.set(0.5)
            frame_eff_1.place_forget()
            frame_eff.place(x= 220, y= 90)       

        def click_submit_button():
            if eff_submit_button.image == button_off_sub:
                eff_submit_button.config(image= button_on_sub)
                eff_submit_button.image = button_on_sub
                #submit is running
                frame_eff_1.place(x= 220, y= 90) 
                eff_text_1.place(x=200,y=5)
                
                # create progressbar
                s=ttk.Style()
                # s.theme_use('clam')
                s.configure('bar.Horizontal.TProgressbar',troughcolor = '#F56230')
                #Int value goes into progressbar
                #progressbar needs 3 steps, start, update(while loop gets variable from childprocess), and stop
                progressbar_var.set(0)
                #the max value of progressbar = global iteration = 200 here but not sure why only 162 in the test
                eff_progressbar = ttk.Progressbar(frame_eff_1,style='bar.Horizontal.TProgressbar',variable=progressbar_var, maximum =epochs_var.get(),length = 350,mode='determinate')
                eff_progressbar.place(x=115,y=80)
                Label(frame_eff_1,textvariable=eff_running_state,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=200,y=50) 
                Label(frame_eff_1,textvariable= progressbar_pers_var,font= ("Arial",14), fg = 'white',bg='#abb2b9').place(x=280,y=150) 
                #avg_global accu and los 
                Label(frame_eff_1,text = "Average Global Accurancy = ",font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=100,y=200) 
                Label(frame_eff_1,text = "Average Global Loss = ",font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=100,y=250) 
                Label(frame_eff_1,textvariable= avg_glob_accu_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=350,y=200) 
                Label(frame_eff_1,textvariable= avg_glob_los_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=300,y=250)  
                check_dataset()
                button_gene=Button(frame_eff_1,text = "Generate or Run", command=generate_or_run_effectiveness_algorithm)
                button_save=Button(frame_eff_1,text = "open result", command= open_file)
                button_plot=Button(frame_eff_1,text = "Plot result", command= plot_result)
                button_back=Button(frame_eff_1,text = "back", command= back_page)
                button_save.place(x=200,y=320)
                button_gene.place(x=50, y = 320) 
                button_plot.place(x=390, y = 320) 
                button_back.place(x=315, y=320)
                #save result
                
            
            else:              
                 eff_submit_button.config(image= button_off_sub)
                 eff_submit_button.image = button_off_sub
                 frame_eff.place_forget()               
   
        
            
    #submit button on the eff frames
        eff_submit_button = Button(frame_eff,image = button_off_sub, border=0,highlightthickness=0,bg='#abb2b9',activebackground = '#abb2b9',command=click_submit_button)
        eff_submit_button.image =button_off_sub 
        eff_submit_button.place(x=250,y=330) 
    
      
    else:
        button_left_main_eff.config(image = button_off_eff)
        button_left_main_eff.image = button_off_eff
        frame_eff.place_forget()
        frame_eff_1.place_forget()
        frame_eff_2.place_forget()

 
def click_privacy_button():
    if button_left_main_pr.image == button_off_pr:
        #click
        button_left_main_pr.config(image= button_on_pr)
        button_left_main_pr.image = button_on_pr       
        frame_pr.place(x= 220, y= 90)    
        pr_text.place(x=200,y=5)

        #variables
        model_var = StringVar()
        image_dataset_var = StringVar()
        dtype_var = StringVar()
        cost_fn_var = StringVar()
        epochs_image_var = StringVar()
        target_id_var = StringVar()
        target_id_var.set("-1")

        def run_image():
            os.chdir("/home/yinbo/Desktop/comp6130/final project/final project/invertinggradients-master/")
            #python3 reconstruct_image.py --model ResNet20-4 --dataset CIFAR10 --trained_model --cost_fn sim --indices def --restarts 32 --save_image --target_id -1
            CLI_command_run_image=["python3", "reconstruct_image.py", "--model", str(model_var.get()), "--dataset", str(image_dataset_var.get()), \
                        "--trained_model", "--cost_fn", str(cost_fn_var.get()), "--epochs", str(epochs_image_var.get()) ,"--indices", "def", "--restarts", "32", \
                        "--save_image", "--target_id", str(target_id_var.get())]
            sub_run_image = subprocess.Popen(CLI_command_run_image,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            # tips, tips_err = sub_run_image.communicate()
            # print (tips)
            while sub_run_image.poll() is None:   
                    info = sub_run_image.stdout.readline()
                    print(info)
        def show_image():
            os.chdir("/home/yinbo/Desktop/comp6130/final project/final project/invertinggradients-master/images")
            resized_groundtrue = PhotoImage(file = '/home/yinbo/Desktop/comp6130/final project/final project/invertinggradients-master/images/a_ground_truth--1.png')
            result_image = PhotoImage(file = f'a_trained{model_var.get()}_{cost_fn_var.get()}-{str(target_id_var.get())}.png')
            groundture_image_lable = Label(frame_pr,image = resized_groundtrue)
            groundture_image_lable.image = resized_groundtrue
            groundture_image_lable.place(x=350,y=100)
            result_image_lable = Label(frame_pr,image= result_image)
            result_image_lable.image = result_image
            result_image_lable.place(x=350,y=200)
            root.update_idletasks() 
            os.chdir("/home/yinbo/Desktop/comp6130/final project/final project/invertinggradients-master/tables/") 
            os.system("nano "+ "table_exp_iv.csv")
            

        Label(frame_pr,text="model",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=70,y=200)
        ttk.Combobox(frame_pr,textvariable= model_var,values = ["ConvNet","ResNet20-4","ResNet18" ,"ResNet152"],width=10).place(x=50,y=220)
        Label(frame_pr,text="dataset",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=70,y=250)
        ttk.Combobox(frame_pr,textvariable= image_dataset_var,values = ["CIFAR10","ImageNet"],width=10).place(x=50,y=270)
        Label(frame_pr,text="dtype",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=70,y=300)
        ttk.Combobox(frame_pr,textvariable= dtype_var,values = ["float","double","half","float64","float16"],width=10).place(x=50,y=320)
        Label(frame_pr,text="costF",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=200,y=200)
        ttk.Combobox(frame_pr,textvariable= cost_fn_var,values = ["sim"],width=10).place(x=180,y=220)
        Label(frame_pr,text="id",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=200,y=320)
        Entry(frame_pr,textvariable=target_id_var,width=5).place(x=230, y=320)

        Label(frame_pr,text="epochs",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=200,y=250)
        ttk.Combobox(frame_pr,textvariable= epochs_image_var,values = ["200","120","100","50","10","1"],width=10).place(x=180,y=270)
        button_image_run=Button(frame_pr,text = "Run", command=run_image)
        button_image_run.place(x=350,y=340)
        button_image_show=Button(frame_pr,text = "Show result", command=show_image)
        button_image_show.place(x=430,y=340)

         
    else:
        button_left_main_pr.config(image = button_off_pr)
        button_left_main_pr.image = button_off_pr
        frame_pr.place_forget()



root.title('COMP6130 Final Project_Group 8')
root.geometry('800x500')
root.config(bg='#083053')
root.resizable(0,0)
#text
topic_text = Label(root,text="Trustworthy Fedrated Learning",font= ("Arial",25), fg = 'white',bg='#083053')
topic_text.place(x=180,y=15)
#input logo and icon 
logo_image = PhotoImage(file = '/home/yinbo/Desktop/comp6130/final project/final project/icon/logo.png')
line_image = PhotoImage(file = '/home/yinbo/Desktop/comp6130/final project/final project/icon/line.png')
button_on_eff = PhotoImage( file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/eff_on.png')
button_off_eff = PhotoImage(file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/eff_off.png')
button_on_pr = PhotoImage( file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/pr_on.png')
button_off_pr = PhotoImage(file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/pr_off.png')
button_on_fa = PhotoImage( file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/fa_on.png')
button_off_fa = PhotoImage(file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/fa_off.png')
button_on_ro = PhotoImage( file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/ro_on.png')
button_off_ro = PhotoImage(file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/ro_off.png')
#button for eff setings submit
button_on_sub = PhotoImage( file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/sub_on.png')
button_off_sub = PhotoImage(file= '/home/yinbo/Desktop/comp6130/final project/final project/icon/sub_off.png')

progressbar_image = Image.open('/home/yinbo/Desktop/comp6130/final project/final project/icon/progressbar_image.png')
progressbar_resized = progressbar_image.resize((370, 30), Image.ANTIALIAS)
progressbar_image = ImageTk.PhotoImage(progressbar_resized)
#blue main canvas
#f = Frame(root, width=800, height=500,bg='#083053')
#f.pack()

#orange part of background
orange_background = Canvas(root,bg='#F56230', width= 200, height=430,border=0,highlightthickness=0)
logo_image_lable = Label(orange_background,image=logo_image,width = 200, height = 80, bd=0,highlightthickness=0,bg='#F56230')
line_image_lable = Label(root,image=line_image,bd=0,highlightthickness=0,bg='#083053')
line_image_lable.place(x=0,y=63)
orange_background.place(x=0, y=70)
logo_image_lable.place(x=0,y=360)
# orange_background.pack()

#buttons on orange part
#testbutton = orange_background.create_image(70,150,image=button_off)
button_left_main_eff = Button(orange_background,image = button_off_eff, border=0,highlightthickness=0,bg='#F56230',activebackground = '#F56230',command=click_effectiveness_button)
button_left_main_pr = Button(orange_background,image = button_off_pr, border=0,highlightthickness=0,bg='#F56230',activebackground = '#F56230',command=click_privacy_button)
button_left_main_ro = Button(orange_background,image = button_off_ro, border=0,highlightthickness=0,bg='#F56230',activebackground = '#F56230',command=click_privacy_button)
button_left_main_fa = Button(orange_background,image = button_off_fa, border=0,highlightthickness=0,bg='#F56230',activebackground = '#F56230',command=click_effectiveness_button)
#testbutton.config(bg='#F56230')
button_left_main_eff.image = button_off_eff
button_left_main_pr.image = button_off_pr
button_left_main_eff.place(x=20,y=40)
button_left_main_pr.place(x=20,y=110)
button_left_main_ro.place(x=20,y=180)
button_left_main_fa.place(x=20,y=250)

#rigth side white area
#effectiveness frame
frame_eff = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
frame_eff_1 = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
frame_eff_2 = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)

eff_text = Label(frame_eff,text="Effectiveness",font= ("Arial",18), fg = '#083053',bg='#abb2b9')
eff_text_1 = Label(frame_eff_1,text="Effectiveness",font= ("Arial",18), fg = '#083053',bg='#abb2b9')
eff_text_2 = Label(frame_eff_2,text="Effectiveness",font= ("Arial",18), fg = '#083053',bg='#abb2b9')

eff_number_clients = Label(frame_eff,text="Number of Clients",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
eff_dataset = Label(frame_eff,text="Dataset",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
eff_learning_rate = Label(frame_eff,text="Learning Rate",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
eff_alpha = Label(frame_eff,text="Alpha",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
eff_total_epochs = Label(frame_eff,text="Total Epochs",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
eff_algo = Label(frame_eff,text="Algorithms",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
eff_r = Label(frame_eff,text="R",font= ("Arial",12), fg = '#083053',bg='#abb2b9')

#progressbar style

Label(frame_eff_1,image=progressbar_image,bg='#abb2b9').place(x=110,y=105)
#privacy frame
frame_pr = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
pr_text = Label(frame_pr,text="Privacy",font= ("Arial",18), fg = '#083053',bg='#abb2b9')

#load car image
left_image = Image.open('/home/yinbo/Desktop/comp6130/final project/final project/invertinggradients-master/auto.jpg')
left_resized = left_image.resize((100, 100), Image.ANTIALIAS)
left_image = ImageTk.PhotoImage(left_resized)
Label(frame_pr,image=left_image,fg = '#083053',bg='#abb2b9').place(x=100,y=70)
Label(frame_pr,text="Ground True",fg = '#083053',bg='#abb2b9').place(x=110,y=170)


#robustness frame


#fairness frame


root.mainloop()
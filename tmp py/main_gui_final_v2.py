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
#Please change to local path before execute this application
#Yinbo_Chen
path = "/home/yinbo/Desktop/comp6130/final project/final project"

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
        r_var.set(0.2)
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
            os.chdir(f"{path}/FedGen-main/data/{dataset_var.get()}") 
            if os.path.isdir(f"u20c10-alpha{alpha_var.get()}-ratio{r_var.get()}") or os.path.isdir(f"u20-letters-alpha{alpha_var.get()}-ratio{r_var.get()}"):   
                eff_running_state.set(f"Found {dataset_var.get()} Dataset! Press run!")
                flag.set(True)
            else:
                eff_running_state.set(f"Please generate {dataset_var.get()} Dataset!")
                flag.set(False)
                

        #generating child process to execute CLI command
        def generate_or_run_effectiveness_algorithm():
            os.chdir(f"{path}/FedGen-main/data/{dataset_var.get()}") 
            if flag.get() ==False:
                eff_running_state.set(f"Generating {dataset_var.get()} Dataset!!!")
                CLI_command_create_data = ["python3", "generate_niid_dirichlet.py", "--n_class", "10","--sampling_ratio", str(r_var.get()), "--alpha", str(alpha_var.get()), "--n_user", "20"]     
                generate_data = subprocess.Popen(CLI_command_create_data)
                generate_data.wait()
                eff_running_state.set(f"Starting {dataset_var.get()} Dataset computing!")          
                os.chdir(path+"/FedGen-main/") 
                flag.set(True)
                root.update_idletasks()
            else:
                os.chdir(path+"/FedGen-main/") 
                #FedGen, FedAvg,FedProx, and FedDistll-FL
                #cli_command_run_data, currently,it's hard coded, for the testing purpose. 
                #CLI_command_run_data = ["python3", "main.py", "--dataset", str(dataset_var.get()) + "-alpha" + str(alpha_var.get()) + "-ratio" + str(r_var.get()), "--algorithm", "FedAvg", "--batch_size", "32", "--num_glob_iters", "200", "--local_epochs", "20", "--num_users", {number_clients_var.get()}, "--lamda", "1", "--learning_rate", "0.01", "--model", "cnn", "--personal_learning_rate", "0.01", "--times", "1"]
                CLI_command_run_data=["python3", "main.py", "--dataset", str(dataset_var.get()) + "-alpha" + str(alpha_var.get()) + 
                        "-ratio" + str(r_var.get()), "--algorithm", str(algo_var.get()), "--batch_size", "32", "--num_glob_iters", str(epochs_var.get()), \
                        "--local_epochs", "20", "--num_users", str(number_clients_var.get()), "--lamda", "1", "--learning_rate", str(learning_rate_var.get()), \
                        "--model", "cnn", "--personal_learning_rate", "0.01", "--times", "3"]
                print(CLI_command_run_data)
                #subprocess.run()
                run_data = subprocess.Popen(CLI_command_run_data,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                #progressbar persantage% =  count/num_glob_iters* times* 100
                eff_running_state.set(f"Starting {dataset_var.get()} Dataset computing!") 
                count = 0
                os.chdir(path+"/txt_results") 
                file_name.set(f"{dataset_var.get()}-alpha{alpha_var.get()}-ratio{r_var.get()}{str(algo_var.get())}-batch_size32-num_glob_iters{epochs_var.get()}--num_users10--learning_rate{learning_rate_var.get()}.txt")
                file= open(file_name.get(),'w')
                for line in iter(run_data.stdout.readline,b''):
                    time.sleep(0.01)
                    root.update_idletasks()
                    info = line.decode("utf-8", "ignore")
                    print(info)
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
                    if count >=100:
                        count = 0

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
            aglo1_combobox= ttk.Combobox(frame_eff_2,textvariable= algo_2_var,values = [",FedGen",",FedAvg",",FedProx",",FedDistll-FL"],width=10).place(x=175,y=100)
            aglo1_combobox= ttk.Combobox(frame_eff_2,textvariable= algo_3_var,values = [",FedGen",",FedAvg",",FedProx",",FedDistll-FL"],width=10).place(x=300,y=100)
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
            Button(frame_eff_2,text= "Plot", command=show_plot).place(x=420,y=300)
            
            

        def open_file():
            os.chdir(path+"/txt_results") 
            os.system("nano "+ file_name.get())
        
        def show_plot():
                os.chdir(path+"/FedGen-main/") 
                #python3 main_plot.py --dataset EMnist-alpha0.1-ratio0.1 --algorithms FedAvg,FedGen --batch_size 32 --local_epochs 20 --num_users 10 --num_glob_iters 200 --plot_legend 1
                CLI_command_plot_data=["python3", "main_plot.py", "--dataset", str(dataset_var.get()) + "-alpha" + str(alpha_var.get()) + 
                        "-ratio" + str(r_var.get()), "--algorithm", str(algo_1_var.get())+str(algo_2_var.get())+str(algo_3_var.get()),\
                        "--batch_size", "32", "--local_epochs", "20", "--num_users",str(number_clients_var.get()),\
                        "--num_glob_iters",str(epochs_var.get()),"--plot_legend", "1"]
                print(CLI_command_plot_data)
                plot_data = subprocess.Popen(CLI_command_plot_data,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                tips, tips_err = plot_data.communicate()
                print (tips_err)
                plot_data.wait
                os.chdir(f"{path}/FedGen-main/figs/{dataset_var.get()}/ratio{r_var.get()}/") 
                
                comparison_images = Image.open(f"{dataset_var.get()}-ratio{r_var.get()}.png")
                progressbar_resized = comparison_images.resize((370, 270), Image.ANTIALIAS)
                comparison_images = ImageTk.PhotoImage(progressbar_resized)
                image_lable_plot = Label(frame_eff_2,image = comparison_images)
                image_lable_plot.image = comparison_images
                image_lable_plot.place(x=20,y=130)

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
            r_var.set(0.2)
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
            os.chdir(path+"/invertinggradients-master/")
            #python3 reconstruct_image.py --model ResNet20-4 --dataset CIFAR10 --trained_model --cost_fn sim --indices def --restarts 32 --save_image --target_id -1
            CLI_command_run_image=["python3", "reconstruct_image.py", "--model", str(model_var.get()), "--dataset", str(image_dataset_var.get()), \
                        "--trained_model", "--cost_fn", str(cost_fn_var.get()), "--epochs", str(epochs_image_var.get()) ,"--indices", "def", "--restarts", "32", \
                        "--save_image", "--target_id", str(target_id_var.get())]
            sub_run_image = subprocess.Popen(CLI_command_run_image,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            # tips, tips_err = sub_run_image.communicate()
            # print (tips)
            # while sub_run_image.poll() is None:   
            #         info = sub_run_image.stdout.readline()
            #         print(info)
        def show_image():
            os.chdir(path+"/invertinggradients-master/images")
            resized_groundtrue = PhotoImage(file = path+'/invertinggradients-master/images/a_ground_truth--1.png')
            result_image = PhotoImage(file = f'a_trained{model_var.get()}_{cost_fn_var.get()}-{str(target_id_var.get())}.png')
            groundture_image_lable = Label(frame_pr,image = resized_groundtrue)
            groundture_image_lable.image = resized_groundtrue
            groundture_image_lable.place(x=350,y=100)
            result_image_lable = Label(frame_pr,image= result_image)
            result_image_lable.image = result_image
            result_image_lable.place(x=470,y=100)
            root.update_idletasks() 
            os.chdir(path+"/invertinggradients-master/tables/") 
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

def click_robustness_button():
    if button_left_main_ro.image == button_off_ro:
        #click
        button_left_main_ro.config(image= button_on_ro)
        button_left_main_ro.image = button_on_ro       
        frame_ro.place(x= 220, y= 90)    
        ro_text.place(x=200,y=5)

        #variables
        algo_var = StringVar()
        algo_var.set("")
        trials_var = IntVar()
        trials_var.set(10)
        
        ro_running_state = StringVar()
        flag = BooleanVar()
        progressbar_text_robuatness_var = StringVar()
        progressbar_text_robuatness_var.set("00%")
        progressbar_robustness_var = IntVar()
        backprop_attack_var = DoubleVar()
        rand_attack_var = DoubleVar()
        file_name = StringVar()
        result_text1_var = StringVar()    
        result_text2_var = StringVar()

        # if str(algo_var.get()) == "ESA":
        #     result_text1.set = "Back propagation attack"
        #     result_text2 = "Random guess attack"
        # elif str(algo_var.get()) == "PRA":
        #     result_text1 = "Path restriction attack"
        #     result_text2 = "Random guess attack"
        # elif str(algo_var.get()) == "GRNA":
        #     result_text1= ""
        #     result_text2 = ""
            
        #generating child process to execute CLI command
        def generate_or_run_robustness_algorithm():
            CLI_command_run=""
            #resultsLabel.set("")
            if str(algo_var.get()) == "ESA":
                os.chdir(path+"/featureinference-vfl-master/ESA/")
                CLI_command_run = ["python3" ,"main-esa.py"]
                #CLI_command_run = "python main-esa.py"
                result_text1_var.set("Back propagation attack")
                result_text2_var.set("Random guess attack")
                root.update_idletasks()
            elif str(algo_var.get()) == "PRA":
                os.chdir(path+"/featureinference-vfl-master/PRA/")
                CLI_command_run=["python3", "main-pra.py"]
                #CLI_command_run = "python main-pra.py"
                result_text1_var.set("Path restriction attack")
                result_text2_var.set("Random guess attack")
                root.update_idletasks()
            elif str(algo_var.get()) == "GRNA":
                os.chdir(path+"/featureinference-vfl-master/GRNA/")
                CLI_command_run=["python3","main-grna.py"]
                #CLI_command_run = "python main-grna.py"
                result_text1_var.set("Mean generator loss: ")
                result_text2_var.set("Mean random guess loss: ")
                root.update_idletasks()
           #os.system(CLI_command_run)
            run_ro_data = subprocess.Popen(CLI_command_run,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            count_trials = 0
            #to execute this part search and count code, you need to change the each main-xxx.py, adding print() result, the original use logging()
            if str(algo_var.get()) == "ESA":
                trials = 'Attack trial'
            elif str(algo_var.get()) == "PRA":
                trials = 'Attack trial'
            elif str(algo_var.get()) == "GRNA":
                trials = '-- Running count:'
            file_name.set(f"{algo_var.get()}.txt")
            file= open(file_name.get(),'w')
            for line in iter(run_ro_data.stdout.readline,b''):
                 time.sleep(0.1)
                 root.update_idletasks()
                 info = line.decode("utf-8", "ignore")
                 file.write(info)
                 print(info)                
                 if re.search(trials,info):
                     count_trials = count_trials+1
                     progressbar_robustness_var.set(count_trials) 
                     temp = count_trials/(trials_var.get()) * 100
                     progressbar_text_robuatness_var.set(str(temp)+"%")
                     print (count_trials)
                 elif re.search(result_text1_var.get(),info):
                     v1 = re.findall(r'\d+.\d+',info)
                     backprop_attack_var.set(v1)
                     root.update_idletasks()
                 elif re.search(result_text2_var.get(),info):
                     v2 = re.findall(r'\d+.\d+',info)
                     rand_attack_var.set(v2)
                     root.update_idletasks()
            file.close()

        def robustness_plot_result():
            #frame_ro.place_forget()
            #frame_ro_1.place_forget()
            #frame_ro_2.place(x= 220, y= 90)
            #ro_text_2.place(x=200,y=5)

            #built enties for each parameter
            entry_trials = Entry(frame_ro,textvariable= trials_var,width=10).place(x= 200, y=100)
            algo_combobox= ttk.Combobox(frame_ro,textvariable= algo_var,values = ["ESA","PRA","GRNA"],width=10).place(x=410,y=100)
            #entry_learning_rate = Entry(frame_eff,textvariable=learning_rate_var,width=10).place(x= 180, y=160)
          
            Label(frame_ro,text="Number of Trials",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            Label(frame_ro,text="Algorithim",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            #Label(frame_eff_2,text="Learning Rate",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            Label(frame_ro,text="Results",font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            #Label(frame_ro,text=results,font= ("Arial",12), fg = '#083053',bg='#abb2b9')
            #Button(frame_ro,text= "Plot", command=show_plot).place(x=420,y=300)

        def open_robustness_log():
            if str(algo_var.get()) == "ESA":
                os.chdir(path+"/featureinference-vfl-master/ESA/log/")
                os.system("nano "+ "bank_unknown_10_expnum_10_*")
            elif str(algo_var.get()) == "PRA":
                os.chdir(path+"/featureinference-vfl-master/PRA/log/")
                os.system("nano "+ "bank_unknown_6_depth_5_expnum_10_*")
            elif str(algo_var.get()) == "GRNA":
                os.chdir(path+"/featureinference-vfl-master/GRNA/log/")
                os.system("nano "+ "drive-*")
           

        #Design Part2
        Label(frame_ro,text="Algorithms",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=90,y=170)
        ttk.Combobox(frame_ro,textvariable= algo_var,values = ["ESA","PRA","GRNA"],width=10).place(x=90,y=200)
        
        Label(frame_ro,text="Attack Trials",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=300,y=170)
        Entry(frame_ro,textvariable=trials_var,width=5).place(x=300, y=200)
        Label(frame_ro_1,image=progressbar_image,bg='#abb2b9').place(x=110,y=105)
        Label(frame_ro,image=progressbar_image,bg='#abb2b9').place(x=95,y=90)
    
        # create progressbar
        s=ttk.Style()
        # s.theme_use('clam')
        s.configure('bar.Horizontal.TProgressbar',troughcolor = '#F56230')
        #Int value goes into progressbar
        #progressbar needs 3 steps, start, update(while loop gets variable from childprocess), and stop
        progressbar_robustness_var.set(0)
        #the max value of progressbar = global iteration = 200 here but not sure why only 162 in the test
        ro_progressbar = ttk.Progressbar(frame_ro,style='bar.Horizontal.TProgressbar',variable=progressbar_robustness_var, maximum =trials_var.get(),length = 350,mode='determinate')
        ro_progressbar.place(x=100,y=60)
        #Label(frame_ro_1,textvariable=eff_running_state,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=200,y=50) 
        Label(frame_ro,textvariable= progressbar_text_robuatness_var,font= ("Arial",14), fg = 'white',bg='#abb2b9').place(x=250,y=140) 
        #avg_global attack 
        Label(frame_ro,textvariable = result_text1_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=100,y=240) 
        Label(frame_ro,textvariable = result_text2_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=100,y=280) 
        Label(frame_ro,textvariable= backprop_attack_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=350,y=240) 
        Label(frame_ro,textvariable= rand_attack_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=350,y=280)  
        #check_dataset()
        button_gene=Button(frame_ro,text = "Run Algorithm", command=generate_or_run_robustness_algorithm)
        button_save=Button(frame_ro,text = "open result", command= open_robustness_log)
        button_save.place(x=300,y=320)
        button_gene.place(x=100, y =320) 
           
    else:
        button_left_main_ro.config(image = button_off_ro)
        button_left_main_ro.image = button_off_ro
        frame_ro.place_forget()
        frame_ro_1.place_forget()
        frame_ro_2.place_forget() 

def click_fairness_button():
    #click
    if button_left_main_fa.image == button_off_fa:
        #click
        button_left_main_fa.config(image= button_on_fa)
        button_left_main_fa.image = button_on_fa       
        frame_fair.place(x= 220, y= 90)    
        fa_text.place(x=230,y=5)

        #vairables of fairness frames
        fairness_flag = BooleanVar()
        fairness_running_state = StringVar()
        model_fairness_var = StringVar()
        method_var = StringVar()
        num_rounds_var = StringVar()
        num_epochs_var = StringVar()
        learning_rate_var = StringVar()
        proportion_var = StringVar()
        # batch_size_var = StringVar()
        train_rate_var = StringVar()
        eval_interval_var = StringVar()
        progressbar_fairness_var = IntVar()
        total_time_cost_var = DoubleVar()
        mean_time_cost_var = DoubleVar()
        progressbar_text_fairness_var = StringVar()

        #fairness vars default setting
        num_rounds_var.set("20")
        num_epochs_var.set("5")
        learning_rate_var.set("0.2")
        proportion_var.set("0.2")
        train_rate_var.set("1")
        eval_interval_var.set("1")
        total_time_cost_var.set(0.0)
        mean_time_cost_var.set(0.0)
        progressbar_text_fairness_var.set("00%")


        def check_fairness_dataset():
            os.chdir(path+"/easyFL-main/fedtask") 
            if os.path.isdir("mnist_client100_dist0_beta0_noise0"):   
                fairness_running_state.set("Found Dataset! Press run!")
                fairness_flag.set(True)
            else:
                fairness_running_state.set("Please generate Dataset first!")
                fairness_flag.set(False)

        def generate_fairness_dataset():
            os.chdir(path+"/easyFL-main")
            #generate dataset for fairness
            CLI_command_generate_fairness_dataset=["python3", "generate_fedtask.py"]
            sub_fairness_generate_process = subprocess.Popen(CLI_command_generate_fairness_dataset,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            #sub_fairness_generate_process.wait()
            fairness_running_state.set("Found Dataset! Press run!")
            fairness_flag.set(True)
            root.update_idletasks()
        
        def run_fairness_main():
            os.chdir(path+"/easyFL-main")
            #python main.py --task mnist_client100_dist0_beta0_noise0 --model cnn --method fedavg --num_rounds 20 --num_epochs 5 --learning_rate 0.215 --proportion 0.1 --batch_size 10 --train_rate 1 --eval_interval 1
            CLI_command_fairness_main = ["python3","main.py","--task","mnist_client100_dist0_beta0_noise0","--model",model_fairness_var.get(),"--method",method_var.get(),"--num_rounds", num_rounds_var.get(),\
                                        "--num_epochs", num_epochs_var.get(),"--learning_rate", learning_rate_var.get(),"--proportion", proportion_var.get(),"--batch_size","10","--train_rate", train_rate_var.get(),"--eval_interval",str(eval_interval_var.get())]
            #CLI_command_fairness_main = ["python3", "main.py", "--task", "mnist_client100_dist0_beta0_noise0", "--model", "cnn", "--method", "fedavg", "--num_rounds", "3", "--num_epochs", "1", "--learning_rate", "0.2", "--proportion", "0.1", "--batch_size", "10", "--train_rate", "1", "--eval_interval", "1"]
            print(CLI_command_fairness_main)
            sub_fairness_process = subprocess.Popen(CLI_command_fairness_main,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            count_round = 0
            for line in iter(sub_fairness_process.stdout.readline,b''):
                time.sleep(0.01)
                root.update_idletasks()
                info = line.decode("utf-8", "ignore")
                print(info)
                round = '--Round'
                global_time_cost = 'Total Time Cost'
                mean_time_cost = 'Mean Time Cost Of Each Round'
                if re.search(round,info):
                    count_round = count_round+1                      
                    temp =  (count_round-1)*int(num_epochs_var.get())/(int(num_rounds_var.get())*int(num_epochs_var.get()))*100
                    progressbar_fairness_var.set(temp) 
                    progressbar_text_fairness_var.set(str(temp)+"%")
                    #print (count)
                elif re.search(global_time_cost,info):
                    v1 = re.findall(r'\d+.\d+',info)
                    total_time_cost_var.set(v1)
                elif re.search(mean_time_cost,info):
                    v2 = re.findall(r'\d+.\d+',info)
                    mean_time_cost_var.set(v2)
        #local UI items for fairness frame
            
        def fairness_plot_result():
                os.chdir(path+"/easyFL-main/utils")
                fairness_plot_process = subprocess.Popen(["python3","result_analysis.py"],stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                root.update_idletasks()    

        #fairness progressbar
        fs=ttk.Style()
        # s.theme_use('clam')
        fs.configure('bar.Horizontal.TProgressbar',troughcolor = '#F56230')
        #Int value goes into progressbar
        #progressbar needs 3 steps, start, update(while loop gets variable from childprocess), and stop
        progressbar_fairness_var.set(0)
        fair_progressbar = ttk.Progressbar(frame_fair,style='bar.Horizontal.TProgressbar',variable=progressbar_fairness_var, maximum = 100,length = 400,mode='determinate')
        fair_progressbar.place(x=90,y=100)
        Label(frame_fair,textvariable = progressbar_text_fairness_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=500,y=100) 

        #text total time and mean time
        Label(frame_fair,text = "Total Time Cost = ",font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=100,y=130) 
        Label(frame_fair,text = "Mean Time Cost Per Round = ",font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=100,y=160) 
        Label(frame_fair,textvariable= total_time_cost_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=350,y=130) 
        Label(frame_fair,textvariable= mean_time_cost_var,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=350,y=160) 

        Label(frame_fair,textvariable=fairness_running_state,font= ("Arial",12), fg = 'white',bg='#abb2b9').place(x=180,y=50)
        button_check=Button(frame_fair,text = "Check and generate", command=generate_fairness_dataset)
        button_run=Button(frame_fair,text = "Run", command= run_fairness_main)
        button_view=Button(frame_fair,text = "View results", command= fairness_plot_result)
        # button_plot=Button(frame_eff_1,text = "Plot result", command= plot_result)
        # button_back=Button(frame_eff_1,text = "back", command= back_page)

        Label(frame_fair,text="model",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=50,y=200)
        ttk.Combobox(frame_fair,textvariable= model_fairness_var,values = ["cnn","mlp","resnet18"],width=10).place(x=30,y=220)
        Label(frame_fair,text="method",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=50,y=250)
        ttk.Combobox(frame_fair,textvariable= method_var,values = ["fedavg","fedbase","fedfa","fedfv","fedmgda+","fedprox","qfedavg"],width=10).place(x=30,y=270)
        Label(frame_fair,text="num round",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=310,y=250)
        Entry(frame_fair,textvariable=num_rounds_var,width=10).place(x=300,y=270)
        Label(frame_fair,text="num epochs",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=430,y=200)
        Entry(frame_fair,textvariable=num_epochs_var,width=10).place(x=430,y=220)
        Label(frame_fair,text="learning rate",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=430,y=250)
        Entry(frame_fair,textvariable=learning_rate_var,width=10).place(x=430, y=270)

        Label(frame_fair,text="proportion",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=310,y=200)
        Entry(frame_fair,textvariable=proportion_var,width=10).place(x=300,y=220)
        # Label(frame_fair,text="batch size",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=450,y=200)
        # ttk.Combobox(frame_fair,textvariable= batch_size_var,values = ["CIFAR10","ImageNet"],width=10).place(x=450,y=220)
        Label(frame_fair,text="train rate",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=180,y=250)
        Entry(frame_fair,textvariable=train_rate_var,width=10).place(x=160,y=270)
        # ttk.Combobox(frame_fair,textvariable= train_rate_var,values = ["float","double","half","float64","float16"],width=10).place(x=160,y=270)
        Label(frame_fair,text="eval interval",font= ("Arial",12), fg = '#083053',bg='#abb2b9').place(x=170,y=200)
        Entry(frame_fair,textvariable=eval_interval_var,width=10).place(x=160,y=220)
        
        button_check.place(x=90, y = 320) 
        button_run.place(x=270,y=320)
        button_view.place(x = 350, y=320)
        # button_plot.place(x=390, y = 320) 
        # button_back.place(x=315, y=320)

        #call functions
        check_fairness_dataset()
        #root.update_idletasks() 
             

    else:
        button_left_main_fa.config(image = button_off_fa)
        button_left_main_fa.image = button_off_fa
        frame_fair.place_forget()

     


root.title('COMP6130 Final Project_Group 8')
root.geometry('800x500')
root.config(bg='#083053')
root.resizable(0,0)
#text
topic_text = Label(root,text="Trustworthy Fedrated Learning",font= ("Arial",25), fg = 'white',bg='#083053')
topic_text.place(x=180,y=15)
#input logo and icon 
logo_image = PhotoImage(file = path+'/icon/logo.png')
line_image = PhotoImage(file = path+'/icon/line.png')
button_on_eff = PhotoImage( file= path+'/icon/eff_on.png')
button_off_eff = PhotoImage(file= path+'/icon/eff_off.png')
button_on_pr = PhotoImage( file= path+'/icon/pr_on.png')
button_off_pr = PhotoImage(file= path+'/icon/pr_off.png')
button_on_fa = PhotoImage( file= path+'/icon/fa_on.png')
button_off_fa = PhotoImage(file= path+'/icon/fa_off.png')
button_on_ro = PhotoImage( file= path+'/icon/ro_on.png')
button_off_ro = PhotoImage(file= path+'/icon/ro_off.png')
#button for eff setings submit
button_on_sub = PhotoImage( file= path+'/icon/sub_on.png')
button_off_sub = PhotoImage(file= path+'/icon/sub_off.png')

progressbar_image = Image.open(path+'/icon/progressbar_image.png')
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
button_left_main_ro = Button(orange_background,image = button_off_ro, border=0,highlightthickness=0,bg='#F56230',activebackground = '#F56230',command=click_robustness_button)
button_left_main_fa = Button(orange_background,image = button_off_fa, border=0,highlightthickness=0,bg='#F56230',activebackground = '#F56230',command=click_fairness_button)
#testbutton.config(bg='#F56230')
button_left_main_eff.image = button_off_eff
button_left_main_pr.image = button_off_pr
button_left_main_ro.image = button_off_ro
button_left_main_fa.image = button_off_fa

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
left_image = Image.open(path+'/invertinggradients-master/auto.jpg')
left_resized = left_image.resize((100, 100), Image.ANTIALIAS)
left_image = ImageTk.PhotoImage(left_resized)
Label(frame_pr,image=left_image,fg = '#083053',bg='#abb2b9').place(x=100,y=70)
Label(frame_pr,text="Ground True",fg = '#083053',bg='#abb2b9').place(x=110,y=170)


#robustness frame
frame_ro = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
frame_ro_1 = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
frame_ro_2 = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
ro_text = Label(frame_ro,text="Robustness",font= ("Arial",18), fg = '#083053',bg='#abb2b9')



#fairness frame
frame_fair = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
frame_fair_1 = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)
frame_fair_2 = Frame(root,bg='#abb2b9', width= 560, height=390,border=0,highlightthickness=0)

fa_text = Label(frame_fair,text="Fairness",font= ("Arial",18), fg = '#083053',bg='#abb2b9')
fa_text_1 = Label(frame_fair_1,text="Fairness",font= ("Arial",18), fg = '#083053',bg='#abb2b9')
fa_text_2 = Label(frame_fair_2,text="Fairness",font= ("Arial",18), fg = '#083053',bg='#abb2b9')



root.mainloop()
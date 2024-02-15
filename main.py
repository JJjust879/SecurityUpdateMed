import customtkinter
import sqlite3
from PIL import Image
from CTkMessagebox import CTkMessagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from CTkListbox import CTkListbox
from tkinter import END, ANCHOR
import os

con = sqlite3.connect('db.db')
cur = con.cursor()

root = customtkinter.CTk(fg_color="#87CEEB")
root.title("VitalCare Medical Center")

filepath = r'Images\transparent.ico'
fullfilepath = os.path.join(os.getcwd(), filepath)
#basically kukunin natin yung name ng laptop at kung
#saan makikita yung folder ng mga picture
#na ginagamit natin sa program

root.iconbitmap(fullfilepath)
root.resizable(False, False)

AppWidth = 750
AppHeight = 550

ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()

x = (ScreenWidth / 2) - (AppWidth / 2)
y = (ScreenHeight / 2) - (AppHeight / 2)

root.geometry(f'{AppWidth}x{AppHeight}+{int(x)}+{int(y)}')

tabview = customtkinter.CTkTabview(root, height=550, width=750, fg_color="#87CEEB",
                                   segmented_button_selected_color="#87CEEB")
tabview.pack(padx=10, pady=5)
tabview.add("Patient Profile")
hidetabname = customtkinter.CTkLabel(root, width=200, height=30, text_color="#87CEEB", fg_color="#87CEEB")
hidetabname.place(relx=0.4, rely=0.02)

# Patient Profile Tab Components of Tabview
findp = AutocompleteCombobox(tabview.tab("Patient Profile"), width=10, font=("", 16), )
findp.place(relx=0.01, rely=0.035)
searchp = customtkinter.CTkButton(tabview.tab("Patient Profile"), text="search", text_color="#000000",
                                  hover_color="#FFFFFF", fg_color='#f5f3e6', width=50, command=lambda: patient_prof())
searchp.place(relx=0.215, rely=0.035)

# Patient Profile Name Frame and its Components
ppf_frame = customtkinter.CTkFrame(tabview.tab("Patient Profile"), fg_color="#ffffff", height=430)
ppf_frame.place(relx=0.01, rely=0.13)

ppdf = r"Images\defaultprofile.png"  # profile picture directory file
fullppdf = os.path.join(os.getcwd(), ppdf)
pp = customtkinter.CTkImage(dark_image=Image.open(fullppdf), size=(120, 120))  # profile picture
pp_label = customtkinter.CTkLabel(ppf_frame, image=pp, text=" ")
pp_label.place(relx=0.20, rely=0.04)

name = customtkinter.CTkLabel(ppf_frame, text="Name: ", text_color="#000000")
name.place(relx=0.10, rely=0.35)
age = customtkinter.CTkLabel(ppf_frame, text="Age: ", text_color="#000000")
age.place(relx=0.10, rely=0.45)
gender = customtkinter.CTkLabel(ppf_frame, text="Gender: ", text_color="#000000")
gender.place(relx=0.10, rely=0.55)
bday = customtkinter.CTkLabel(ppf_frame, text="Birthday: ", text_color="#000000")
bday.place(relx=0.10, rely=0.65)
add = customtkinter.CTkLabel(ppf_frame, text="Address: ", text_color="#000000")
add.place(relx=0.10, rely=0.75)
cno = customtkinter.CTkLabel(ppf_frame, text="Cel.No#: ", text_color="#000000")
cno.place(relx=0.10, rely=0.9)
# End of Patient Profile Name Frame and its Components

# Medical Presciption Frame and its Components
mp_frame = customtkinter.CTkFrame(tabview.tab("Patient Profile"), fg_color='#FFFFFF', height=480,
                                  width=515)  # medical prescription
mp_frame.place(relx=0.295, rely=0.03)

rxdf = r"Images\Rx.png"
fullrxdf = os.path.join(os.getcwd(), rxdf)
rx = customtkinter.CTkImage(dark_image=Image.open(fullrxdf), size=(90, 90))  # profile picture
rx_label = customtkinter.CTkLabel(mp_frame, image=rx, text=" ")
rx_label.place(relx=0.06, rely=0.04)
hospital_name = customtkinter.CTkLabel(mp_frame, text="VitalCare Medical Center", font=('Helvetica', 20, 'bold'),
                                       text_color="#000000")
hospital_name.place(relx=0.23, rely=0.055)
hptladd = customtkinter.CTkLabel(mp_frame, text="Roxas St, San Fermin, Cauayan City, Isabela", font=("", 12),
                                 text_color="#000000", fg_color="transparent")
hptladd.place(relx=0.23, rely=0.11)
drname = customtkinter.CTkLabel(mp_frame, text="Dr.Kate", font=("", 14, 'bold'), text_color="#000000",
                                fg_color="transparent")
drname.place(relx=0.85, rely=0.8)
guhit = customtkinter.CTkFrame(mp_frame, fg_color="#000000", height=3, width=380)
guhit.place(relx=0.21, rely=0.17)
guhitsign = customtkinter.CTkFrame(mp_frame, fg_color="#000000", height=3, width=100)
guhitsign.place(relx=0.75, rely=0.78)
# ----------------------------------------------------------------------------------------------------------------
illness = customtkinter.CTkLabel(mp_frame, text="Diagnosis: ", text_color="#000000")
illness.place(relx=0.1, rely=0.2)
dop = customtkinter.CTkLabel(mp_frame, text="Date: ", text_color="#000000")  # date of prescription
dop.place(relx=0.7, rely=0.2)
med = customtkinter.CTkLabel(mp_frame, text="Medication: ", text_color="#000000")  # medication
med.place(relx=0.10, rely=0.3)
dosage = customtkinter.CTkLabel(mp_frame, text="Dosage: ", text_color="#000000")
dosage.place(relx=0.10, rely=0.4)

timesper = customtkinter.CTkLabel(mp_frame, text="Timesper: ", text_color="#000000")
timesper.place(relx=0.10, rely=0.5)
tpd = customtkinter.CTkCheckBox(mp_frame, text="Day", text_color="#000000", onvalue= "on", offvalue="off", state='disabled')  # times per day
tpd.place(relx=0.25, rely=0.5)
tpw = customtkinter.CTkCheckBox(mp_frame, text="Week", text_color="#000000", onvalue= "on", offvalue="off", state='disabled')  # times per week
tpw.place(relx=0.40, rely=0.5)

dotw = customtkinter.CTkLabel(mp_frame, text="Days of the Week: ", text_color="#000000")  # days of the week
dotw.place(relx=0.10, rely=0.58)
mcbx = customtkinter.CTkCheckBox(mp_frame, text="Monday", text_color="#000000", state='disabled')  # monday checkbox
mcbx.place(relx=0.35, rely=0.58)
tcbx = customtkinter.CTkCheckBox(mp_frame, text="Tuesday", text_color="#000000", state='disabled')  # tuesday checkbox
tcbx.place(relx=0.55, rely=0.58)
wcbx = customtkinter.CTkCheckBox(mp_frame, text="Wednesday", text_color="#000000",
                                 state='disabled')  # wednesday checkbox
wcbx.place(relx=0.75, rely=0.58)
thcbx = customtkinter.CTkCheckBox(mp_frame, text="Thursday", text_color="#000000",
                                  state='disabled')  # thursday checkbox
thcbx.place(relx=0.1, rely=0.65)
fcbx = customtkinter.CTkCheckBox(mp_frame, text="Friday", text_color="#000000", state='disabled')  # friday checkbox
fcbx.place(relx=0.3, rely=0.65)
stcbx = customtkinter.CTkCheckBox(mp_frame, text="Saturday", text_color="#000000",
                                  state='disabled')  # saturday checkbox
stcbx.place(relx=0.5, rely=0.65)
sucbx = customtkinter.CTkCheckBox(mp_frame, text="Sunday", text_color="#000000", state='disabled')  # sunday checkbox
sucbx.place(relx=0.7, rely=0.65)

frequency = customtkinter.CTkLabel(mp_frame, text="Frequency: ", text_color="#000000")
frequency.place(relx=0.10, rely=0.73)
time = customtkinter.CTkLabel(mp_frame, text="Time: ", text_color="#000000")
time.place(relx=0.10, rely=0.8)

mf_btn = customtkinter.CTkButton(mp_frame, text="Medication Field", text_color="#000000", width=100,
                                 hover_color="#FFFFFF", fg_color='#fff5ee', command=lambda: medication_field_btn(),
                                 state='disabled')
mf_btn.place(relx=0.1, rely=0.9)
cm_btn = customtkinter.CTkButton(mp_frame, text="Current Medication", width=100,
                                 hover_color="#FFFFFF", fg_color='#f5f3e6', text_color="#000000",
                                 command=lambda: show_message(), state='disabled')
cm_btn.place(relx=0.1, rely=1)
nm_btn = customtkinter.CTkButton(mp_frame, text="New Medication", text_color="#000000", width=100, state='disabled',
                                 hover_color="#FFFFFF", fg_color='#f5f3e6', command=lambda: new_medication())
nm_btn.place(relx=0.1, rely=1)
f_btn = customtkinter.CTkButton(mp_frame, text="Formulary", text_color="#000000", width=100, state='disabled',
                                hover_color="#FFFFFF", fg_color='#f5f3e6', command=lambda: open_formulary())
f_btn.place(relx=0.1, rely=1)

EtrDsg1 = customtkinter.CTkEntry(mp_frame, placeholder_text="Enter Dosage", width=100)
EtrDsg1.place(relx=1, rely=1)
EtrDsg1Btn = customtkinter.CTkButton(mp_frame, text="confirm", text_color="#000000",
                                     hover_color="#FFFFFF", fg_color='#f5f3e6', width=50,
                                     command=lambda: change_dosage(True))
EtrDsg1Btn.place(relx=1, rely=1)
cncl_entrdsg = customtkinter.CTkButton(mp_frame, text="cancel",
                                       hover_color="#FFFFFF", fg_color='#f5f3e6', text_color="#000000", width=50,
                                       command=lambda: change_dosage(False))
cncl_entrdsg.place(relx=1, rely=1)

check = False


# Functions where data is being retrieved-----------------------------------
def patient_prof():
    pid = findp.get()
    EtrDsg1.delete(0, END)
    EtrDsg2.delete(0, END)
    if pid:
        try:
            getinfo = f"""
                        select * from patient_profile where patientid = '{pid.upper()}'
                        """

            cur.execute(getinfo)
            row = cur.fetchall()

            for i in range(len(row)):
                rows = row[i]

            # personal info
            try:
                print(rows[9])
                ppfd = os.path.join(os.getcwd(), rows[9])
                pp.configure(dark_image=Image.open(ppfd))  # profile picture
                pp_label.configure(image=pp, text="")
                name.configure(text=f"Name:      {rows[1]}")
                age.configure(text=f"Age:           {rows[2]}")
                bday.configure(text=f"Birthday:    {rows[3]}")
                gender.configure(text=f"Gender:    {rows[4]}")
                add.configure(text=f"Address:    \n{rows[5]}", justify='left', wraplength=180)
                cno.configure(text=f"Cel.No#:    {rows[6]}")
            except:
                message_format("Error", "Patient has no profile picture")

            patient_medical_record()
        except:
            message_format("Info", "No Data Found\nPlease Check Your ID")
    else:
        message_format("Info", "No Data Found\nPlease Check Your ID")


def patient_medical_record():
    pid = findp.get()

    if pid:
        try:
            query = f"""
                    select * from patient_dosage where patientid = '{pid.upper()}'
                """

            cur.execute(query)
            row = cur.fetchall()

            for i in range(len(row)):
                rows = row[i]

            illness.configure(text=f"Diagnosis: {rows[1]}")
            med.configure(text=f"Medication: {rows[2]}")
            dosage.configure(text=f"Dosage: {rows[3]}{rows[4]}")
            frequency.configure(text=f"Frequency: {rows[7]}")
            time.configure(text=f"Time: {rows[8]}")
            dop.configure(text=f"Date: {rows[9]}")

            # deselect everytime and set state into normal
            tpd.deselect()
            tpd.configure(state='normal')
            tpw.deselect()
            tpw.configure(state='normal')

            if rows[5] == "Day":
                tpd.select()
                tpw.configure(state='disabled')
            else:
                tpw.select()
                tpd.configure(state='disabled')

            monday = "monday" in str(rows[6])
            tuesday = "tuesday" in str(rows[6])
            wednesday = "wednesday" in str(rows[6])
            thursday = "thursday" in str(rows[6])
            friday = "friday" in str(rows[6])
            saturday = "saturday" in str(rows[6])
            sunday = "sunday" in str(rows[6])

            # I need to deselect everytime this function called so the recent selected checkbox will be emplty
            mcbx.deselect()
            tcbx.deselect()
            wcbx.deselect()
            thcbx.deselect()
            fcbx.deselect()
            stcbx.deselect()
            sucbx.deselect()

            mcbx.configure(state="disabled")
            tcbx.configure(state="disabled")
            wcbx.configure(state="disabled")
            thcbx.configure(state="disabled")
            fcbx.configure(state="disabled")
            stcbx.configure(state="disabled")
            sucbx.configure(state="disabled")

            if monday == True:
                mcbx.select()
            else:
                mcbx.configure(state='disabled')

            if tuesday == True:
                tcbx.select()
            else:
                tcbx.configure(state="disabled")

            if wednesday == True:
                wcbx.select()
            else:
                wcbx.configure(state="disabled")

            if thursday == True:
                thcbx.select()
            else:
                thcbx.configure(state='disabled')

            if friday == True:
                fcbx.select()
            else:
                fcbx.configure(state='disabled')

            if saturday == True:
                stcbx.select()
            else:
                stcbx.configure(state='disabled')

            if sunday == "sunday":
                sucbx.select()
            else:
                sucbx.configure(state='disabled')

            mf_btn.configure(state='normal')
            cm_btn.configure(state='normal')
            nm_btn.configure(state='normal')
            f_btn.configure(state='normal')
        except:
            message_format("Info", "No Data Found\nPlease Check Your ID")


def medication_field_btn():  # show other buttons inside medication field
    mf_btn.place(rely=1)
    cm_btn.place(relx=0.1, rely=0.9)
    nm_btn.place(relx=0.41, rely=0.9)
    f_btn.place(relx=0.7, rely=0.9)


def show_message():
    hide_new_medication_elements()
    hide_formulary_elements()
    patient_prof()
    message_format("Asking?", "Would You Like To Change Dosage?")


def change_dosage(changeit):
    if changeit == True:
        nw_dos = EtrDsg1.get()
        NewDosage = int(nw_dos)
        pid = findp.get()

        query0 = f"""
            select medicine from patient_dosage
            where patientid = '{pid}'
        """

        cur.execute(query0)
        MN = cur.fetchall()
        MedicineName = MN[0][0]

        query1 = f"""
                    select minimumdosage from medicine_info
                    where name = '{MedicineName}'
             """
        cur.execute(query1)
        mnmdsgtxt = cur.fetchall()
        mnmdsglst = [e for e, in mnmdsgtxt]
        mnmdsgnum = int(*mnmdsglst)

        query2 = f"""
                            select maximumdosage from medicine_info
                           where name = '{MedicineName}'
                    """
        cur.execute(query2)
        mxmdstxt = cur.fetchall()
        mxmdslst = [e for e, in mxmdstxt]
        mxmdsnum = int(*mxmdslst)

        if NewDosage >= mnmdsgnum and NewDosage <= mxmdsnum:
            query = f""" 
                       update patient_dosage
                       set dosage = '{nw_dos}' 
                       where patientid = '{pid.upper()}'
                       """

            cur.execute(query)
            con.commit()

            patient_prof()

            message_format("Success!", "The Patient Dosage Modification Complete.")
            patient_prof()

        else:
            CTkMessagebox(title=" ", message= "Dosage is not in appropriate range", icon= "cancel")


    else:
        EtrDsg1.place(rely=1)
        EtrDsg1Btn.place(rely=1)
        cncl_entrdsg.place(rely=1)



def message_format(ttl, mess):
    if ttl == "Info":
        CTkMessagebox(title=ttl, message=mess)
    elif ttl == "Asking?":
        mssgbx = CTkMessagebox(title=ttl, message=mess, option_1="No", option_2="Yes", icon="question")

        if mssgbx.get() == "Yes":
            wrng = CTkMessagebox(title="Warning!", message="Please Check the Dosage Carefully\nBefore Entering",
                                 icon="warning", option_1="Ok")

            if wrng.get() == "Ok":
                EtrDsg1.place(relx=0.2, rely=0.4)
                EtrDsg1Btn.place(relx=0.40, rely=0.4)
                cncl_entrdsg.place(relx=0.52, rely=0.4)

    elif ttl == "Success!":
        scss = CTkMessagebox(title=ttl, message=mess, icon="check")
        EtrDsg1.place(rely=1)
        EtrDsg1Btn.place(rely=1)
        cncl_entrdsg.place(rely=1)

        pid = findp.get()
        query = f"""
            select dosage from patient_dosage where patientid = '{pid.upper()}'
        """
        cur.execute(query)
        dosage.configure(text=cur.fetchall())

    elif ttl == "Error":
        error = CTkMessagebox(title=ttl, message=mess, icon="cancel")
    elif ttl == "Question":
        ask = CTkMessagebox(title="Asking", message=mess, icon="question", option_1="No", option_2="Yes")

        if ask.get() == "Yes":
            wrng = CTkMessagebox(title="Warning!",
                                 message="You're about to change the dosage\nPlease check the dosage before entering.",
                                 icon="warning", option_1="Ok")

            if wrng.get() == "Ok":
                SearchMed.configure(placeholder_text="Enter Dosage")
                SearchMed.place(rely=1)
                chng_mdcn_ds.place(relx=0.63, rely=0.33)
                EtrDsg2.place(relx=0.44, rely=0.33)




def loadid_in_autocomplete_entry():
    query = f"""
        select patientid from patient_profile 
"""

    cur.execute(query)
    row = cur.fetchall()
    rows = [e for e, in row]

    findp.configure(completevalues=rows)


# New Medication Elements------------------------------------------------------------------------------------------------
query = f"""
    select name from medicine_info
"""

cur.execute(query)
row = cur.fetchall()
list = [e for e, in row]

SearchMed = customtkinter.CTkEntry(root, placeholder_text="search here")
SearchMed.place(rely=1)
EtrDsg2 = customtkinter.CTkEntry(root, placeholder_text="enter dosage")
EtrDsg2.place(rely=1)
showlists = CTkListbox(root, width=300, text_color="#FFFFFF", fg_color="#000000")
showlists.place(rely=1)
SearchMedBtn = customtkinter.CTkButton(root, text="select", text_color="#000000",
                                    hover_color="#FFFFFF", fg_color='#ffe4c4', width=50,
                                    command=lambda: change_medicine_dosage())
SearchMedBtn.place(rely=1)
chng_mdcn_ds = customtkinter.CTkButton(root, text="change",
                                       hover_color="#FFFFFF", fg_color='#f5f3e6', text_color="#000000", width=50,
                                       command=lambda: update_medicine_dosage())
chng_mdcn_ds.place(rely=1)


def hide_medical_info_and_show_new_medication_btns():
    illness.place(rely=1)
    frequency.place(rely=1)
    timesper.place(rely=1)
    dotw.place(rely=1)
    dop.place(rely=1)
    time.place(rely=1)
    med.place(rely=1)
    dosage.place(rely=1)

    tpd.place(rely=1)
    tpw.place(rely=1)
    mcbx.place(rely=1)
    tcbx.place(rely=1)
    wcbx.place(rely=1)
    thcbx.place(rely=1)
    fcbx.place(rely=1)
    stcbx.place(rely=1)
    sucbx.place(rely=1)

    SearchMed.place(relx=0.44, rely=0.33)
    showlists.place(relx=0.44, rely=0.40)
    SearchMedBtn.place(relx=0.63, rely=0.33)


def hide_new_medication_elements():
    showlists.place(rely=1)
    SearchMedBtn.place(rely=1)
    chng_mdcn_ds.place(rely=1)
    EtrDsg2.place(rely=1)
    SearchMed.place(rely=1)

    show_patient_medical_record_elements()


def show_patient_medical_record_elements():
    illness.place(relx=0.1, rely=0.2)
    dop.place(relx=0.7, rely=0.2)
    med.place(relx=0.10, rely=0.3)
    dosage.place(relx=0.10, rely=0.4)
    timesper.place(relx=0.10, rely=0.5)
    tpd.place(relx=0.25, rely=0.5)
    tpw.place(relx=0.40, rely=0.5)
    dotw.place(relx=0.10, rely=0.58)
    mcbx.place(relx=0.35, rely=0.58)
    tcbx.place(relx=0.55, rely=0.58)
    wcbx.place(relx=0.75, rely=0.58)
    thcbx.place(relx=0.1, rely=0.65)
    fcbx.place(relx=0.3, rely=0.65)
    stcbx.place(relx=0.5, rely=0.65)
    sucbx.place(relx=0.7, rely=0.65)
    frequency.place(relx=0.10, rely=0.73)
    time.place(relx=0.10, rely=0.8)
    mf_btn.place(relx=0.1, rely=0.9)
    rx_label.place(relx=0.06, rely=0.04)
    guhit.place(relx=0.21, rely=0.17)


def new_medication():
    hide_medical_info_and_show_new_medication_btns()
    hide_formulary_elements()

    on_current_med = False
    if on_current_med == False:
        cm_btn.configure(command=lambda: show_message())

    update_data(list)
    showlists.bind("<<ListBoxSelect>>", showlist)
    SearchMed.bind("<KeyRelease>", check)


def change_medicine_dosage():
    mdcn_name = SearchMed.get()

    query = f"""
          select name from medicine_info
          where name = '{mdcn_name}' 
     """

    cur.execute(query)
    MN = cur.fetchall()

    if len(MN) > 0:
        if mdcn_name:
            message_format("Question", "Does the selected medication correct?")
    else:
        CTkMessagebox(title= " ", message= "No medicine found please try again", icon= "warning")


def update_medicine_dosage():
    newmeddosage = EtrDsg2.get()
    NewMedDosage = int(newmeddosage)
    MedicineName = SearchMed.get()
    pid = findp.get()

    query1 = f"""
    select minimumdosage from medicine_info
    where name = '{MedicineName}'
    """
    cur.execute(query1)
    mnmdsgtxt = cur.fetchall()
    mnmdsglst = [e for e, in mnmdsgtxt]
    mnmdsgnum = int(*mnmdsglst)

    query2 = f"""
        select maximumdosage from medicine_info
        where name = '{MedicineName}'
    """
    cur.execute(query2)
    mxmdstxt = cur.fetchall()
    mxmdslst = [e for e, in mxmdstxt]
    mxmdsnum = int(*mxmdslst)

    if NewMedDosage >= mnmdsgnum and NewMedDosage <= mxmdsnum:
        query1 = f""" 
            update medicine_info 
            set dosage = '{NewMedDosage}' 
            where name = '{MedicineName}' 
            """

        cur.execute(query1)
        con.commit()

        query2 = f""" 
                update patient_dosage 
                set dosage = '{NewMedDosage}', medicine = '{MedicineName}' 
                where patientid = '{pid}' 
                """

        cur.execute(query2)
        con.commit()

        message_format("Success!", "Dosage Modification Complete.")
        hide_new_medication_elements()
        patient_prof()

    else:
        CTkMessagebox(title= " ", message= "Medicine dosage is not in appropritate range", icon= "cancel")


def update_data(data):
    if showlists.size() > 0:
        showlists.delete(0, END)
    else:
        for item in data:
            showlists.insert(END, item)


def showlist(event):
    SearchMed.delete(0, END)
    SearchMed.insert(0, showlists.get(ANCHOR))


def check(event):
    # grab what was typed
    typed = SearchMed.get()

    if typed == '':
        data = list
    else:
        data = []
        for item in list:
            if typed.lower() in item.lower():
                data.append(item)

    # update our listbox with selected items
    update_data(data)


# Formulary Elements-----------------------------------------------------------------------------------------------------
chng_ill = customtkinter.CTkEntry(mp_frame)
chng_ill.place(rely=1)
chng_med = customtkinter.CTkEntry(mp_frame)
chng_med.place(rely=1)
dsg_typ = customtkinter.CTkEntry(mp_frame, width=60, placeholder_text="mg/g")
dsg_typ.place(rely=1)
chng_frqncy = customtkinter.CTkEntry(mp_frame)
chng_frqncy.place(rely=1)
chng_tm = customtkinter.CTkEntry(mp_frame)
chng_tm.place(rely=1)
chng_dt = customtkinter.CTkEntry(mp_frame, width=80)
chng_dt.place(rely=1)
svd_fmlry = customtkinter.CTkButton(mp_frame, text='saved',
                                    hover_color="#FFFFFF", fg_color='#f5f3e6', text_color="#000000",
                                    command=lambda: update_data_using_formulary())
svd_fmlry.place(rely=1)


def open_formulary():
    hide_new_medication_elements()

    illness.configure(text="Diagnosis:")
    med.configure(text="Medication:")
    dosage.configure(text="Dosage:")
    frequency.configure(text="Frequency:")
    time.configure(text="Time:")
    dop.configure(text="Data:")

    chng_ill.place(relx=0.25, rely=0.2)
    chng_dt.place(relx=0.78, rely=0.2)
    chng_med.place(relx=0.25, rely=0.3)
    EtrDsg1.place(relx=0.25, rely=0.4)
    dsg_typ.place(relx=0.45, rely=0.4)
    chng_frqncy.place(relx=0.25, rely=0.73)
    chng_tm.place(relx=0.25, rely=0.8)
    svd_fmlry.place(relx=0.7, rely=0.9)

    mcbx.configure(state="normal")
    tcbx.configure(state="normal")
    wcbx.configure(state="normal")
    thcbx.configure(state="normal")
    fcbx.configure(state="normal")
    stcbx.configure(state="normal")
    sucbx.configure(state="normal")
    tpw.configure(state="normal")
    tpd.configure(state="normal")

    mcbx.deselect()
    tcbx.deselect()
    wcbx.deselect()
    thcbx.deselect()
    fcbx.deselect()
    stcbx.deselect()
    sucbx.deselect()
    tpw.deselect()
    tpd.deselect()


def update_data_using_formulary():
    pid = findp.get()
    daysofweek = []
    tmprs = None


    if tpd.get() == "on" and tpw.get() == "off":
        tpw.deselect()
        tmprs = "Day"
        daysofweek.append('N/A')

    elif tpw.get() == "on" and tpd.get() == "off":
        tpd.deselect()
        tmprs = "Week"

        if mcbx.get():
            daysofweek.append('monday')
        if tcbx.get():
            daysofweek.append('tuesday')
        if wcbx.get():
            daysofweek.append('wednesday')
        if thcbx.get():
            daysofweek.append('thursday')
        if fcbx.get():
            daysofweek.append('friday')
        if stcbx.get():
            daysofweek.append('saturday')
        if sucbx.get():
            daysofweek.append('sunday')
    else:
        CTkMessagebox(title= " ", message= "Please only select one betweek Day and Week")

    query1 = f"""
            select minimumdosage from medicine_info
            where name = '{chng_med.get()}'
     """
    cur.execute(query1)
    mnmdsgtxt = cur.fetchall()
    mnmdsglst = [e for e, in mnmdsgtxt]
    mnmdsgnum = int(*mnmdsglst)

    query2 = f"""
                    select maximumdosage from medicine_info
                   where name = '{chng_med.get()}'
            """
    cur.execute(query2)
    mxmdstxt = cur.fetchall()
    mxmdslst = [e for e, in mxmdstxt]
    mxmdsnum = int(*mxmdslst)

    try:
        etr_dsg_num = int(EtrDsg1.get())
        newdos = etr_dsg_num
        newmdctn = chng_med.get()
        newdostyp = dsg_typ.get()
        newdiag = chng_ill.get()
        newtime = chng_tm.get()
        newfrq = chng_frqncy.get()
        newdt = chng_dt.get()
        newtmprs = tmprs
        newdotweek = ' '.join(daysofweek)

        if newdos and newmdctn and newdostyp and newdiag and newtime and newfrq and newdt:
            if etr_dsg_num >= mnmdsgnum and etr_dsg_num <= mxmdsnum:
                query3 = f"""
                        update patient_dosage
                        set illness = '{newdiag}', medicine = '{newmdctn}', dosage = '{newdos}',
                        dosagetype = '{newdostyp}', timesper = '{newtmprs}', daysoftheweek = '{newdotweek}',
                        frequency = '{newfrq}', time = '{newtime}', date = '{newdt}'
                        where patientid = '{pid}' 
                    """
                cur.execute(query3)
                con.commit()
                hide_formulary_elements()
                patient_prof()
            else:
                 CTkMessagebox(title="Danger", icon="cancel", message="The dosage is not in range of the selected medication.")
        else:
            CTkMessagebox(title=" ", message="Please complete the prescription data", icon="cancel")
    except:
     CTkMessagebox(title=" ", message="Please complete the prescription data", icon="cancel")

def hide_formulary_elements():
    chng_ill.place(rely=1)
    chng_dt.place(rely=1)
    chng_med.place(rely=1)
    EtrDsg1.place(rely=1)
    dsg_typ.place(rely=1)
    chng_frqncy.place(rely=1)
    chng_tm.place(rely=1)
    svd_fmlry.place(rely=1)


loadid_in_autocomplete_entry()
# Pwedeng pagkunan ng dataset
# https://www.singlecare.com/blog/most-prescribed-drugs-2022/
root.mainloop()
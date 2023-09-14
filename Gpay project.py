import weakref
from datetime import date

class Database:
    
    Bank_List=['Axis Bank', 'Bank of India', 'City Union Bank', 'HDFC Bank', 'ICICI Bank', 'Indian Bank', 'Indian Overseas Bank', 'Karur Vysya Bank', 'SBI']
    IFSC_Codes=['AXIBSA001','BOIB002','CUBC003','HDFCBD004','ICICIBE005','IDIBF006','IOBG007','KVBH008','SBII009']
    Users=[]

    # it act as login verification
    @staticmethod
    def verify(phone,password):
        for i in range(len(Database.Users)):
            if Database.Users[i].Phone_No==phone and Database.Users[i].Password==password:
                print("---------------------------------------------")
                print("Google Pay Opening....")
                return Database.Users[i]
        else:
            print("Invalid Phone number or Password")
            return False

    @staticmethod
    def is_new_user(phone):
        for i in range(len(Database.Users)):
            if Database.Users[i].Phone_No==phone:
                return False
        else:
            return True
        
        
    @staticmethod
    def valid_email(email):
        for i in range(len(Database.Users)):
            if Database.Users[i].Email==email:
                password=input("Enter New password : ")
                confirm=input("Enter Confirm password : ")
                if password==confirm:
                    Database.Users[i].Password==password
                    return True
                else:
                    print('\u274e',end=" ")
                    print("Password not match ")
                    return False
                    

        else:
            print('\u274e',end=" ")
            print("Email id not found")
            return False
    # it shows all bank from the Database
    @classmethod
    def show_bank_list(cls):
        print("---------------------------------------------")
        index=1
        for i in cls.Bank_List:
            print(index," - ",i)
            index+=1
    

    
class Bank_Details:

    def __init__(self,bank_name,ifsc,account_no,upi_id,pin,balance):
        self.Bank_Name=bank_name
        self.IFSC_Code=ifsc
        self.Account_No=account_no
        self.UPI_ID=upi_id
        self.PIN=pin
        self.Balance=balance

    # it shows the user linked banks
    def show_linked_bank(self):
        print("Your Linked Bank Accounts :")
        index=1        
        for j in range(len(self.Bank_Accounts)):
            print(index," - ",self.Bank_Accounts[j].Bank_Name)
            index+=1

    # it add bank account in GPAY
    def add_bank(self):
        print("---------------------------------------------")
        print("Choose the Bank: ")
        Database.show_bank_list()
        choice=int(input("Enter the choice: "))
        if not 1<=choice<=9:
            print("Invalid Choice")
            return
        bank_name=Database.Bank_List[choice-1]
        for i in range(len(self.Bank_Accounts)):
            if bank_name == self.Bank_Accounts[i].Bank_Name:
                print('\u274e',end=" ")
                print("Bank account aldready linked")
                break            
        else:
            account_no=int(input("Enter Account Number: "))
            ifsc=Database.IFSC_Codes[choice-1]
            upi_id=input("Enter UPI id: ")
            pin=input("Enter PIN: ")
            balance=float(input("Enter Balance: "))
            ac=Bank_Details(bank_name,ifsc,account_no,upi_id,pin,balance)
            self.Bank_Accounts.append(ac)
            print('\u2705',end=" ")
            print("Bank account Added successfully")
            
    # it is a dummy method for adding bank account for the user
    # for explanation purpose only
    def add_bank_direct(self,bank_name,ifsc,account_no,upi_id,pin,balance):
        ac=Bank_Details(bank_name,ifsc,account_no,upi_id,pin,balance)
        self.Bank_Accounts.append(ac)
        print('\u2705',end=" ")
        print("Bank account Added successfully")

    # it remove bank from GPAY 
    def remove_bank(self):
        print("---------------------------------------------")
        index=1
        for i in range(len(self.Bank_Accounts)):
            print(index," - ",self.Bank_Accounts[i].Bank_Name)
            index+=1        
        choice=int(input("Enter the choice: "))
        if not (1<=choice<=len(self.Bank_Accounts)):
            print("Invalid choice")
            return
        del self.Bank_Accounts[choice-1]
        print('\u2705',end=" ")
        print("Bank account removed successfully")

    def verify_pin(self,bank):
        pin=input("Enter Account PIN : ")
        if self.Bank_Accounts[bank].PIN==pin:
            return True
        else:
            return False

    def modify_pin(self):
        index=1
        for i in range(len(self.Bank_Accounts)):
            print(index," - ",self.Bank_Accounts[i].Bank_Name)
            index+=1        
        choice=int(input("Enter the choice: "))
        if not (1<=choice<=len(self.Bank_Accounts)):
            print("Invalid choice")
            return
        pin=input("Enter current PIN : ")
        if self.Bank_Accounts[choice-1].PIN==pin:
            pin=input("Enter New PIN : ")
            confirm=input("Enter confirm PIN : ")
            if pin==confirm:
                self.Bank_Accounts[i].PIN=pin
                print('\u2705',end=" ")
                print("PIN changed successfully")
            else:
                print('\u274e',end=" ")
                print("New PIN and confirm PIN not matched")
        else:
            print('\u274e',end=" ")
            print("Invalid PIN")


    def check_balance(self):
        self.show_linked_bank()
        choice=int(input("Choose your choice: "))
        if not(1<=choice<=len(self.Bank_Accounts)):
            print("Invalid choice")
            return
        else:
            ver=self.verify_pin(choice-1)
            if ver:
                print(self.Bank_Accounts[choice-1].Balance)
        
class Transactions:
    
    def __init__(self,date,send_bank,sender,receive_bank,receiver,medium,balance):
        self.Date=date
        self.Send_Bank=send_bank
        self.Sender=sender
        self.Receive_Bank=receive_bank
        self.Receiver=receiver
        self.Medium=medium
        self.Balance=balance
        #self.__class__.Transaction_History.append(weakref.proxy(self))

    # it is important method for storing the transaction history
    def bank_transfer_process(self,to_user,to_bank,medium,amount):
        self.show_linked_bank()
        choice=int(input("Choose your choice"))
        if not(1<=choice<=len(self.Bank_Accounts)):
            print("invalid choice")
            return
        else:
            sender=self.Bank_Accounts[choice-1]
            ver=self.verify_pin(choice-1)
            if ver==False:
                print("Incorrect Acount PIN")
            else:
                if sender.Balance>=amount:
                    sender.Balance-=amount
                else:
                    print('\u274e',end=" ")
                    print("Transaction Unsuccessful: Insufficient Balance")
                    return 
                receiver_bank=Database.Users[to_user].Bank_Accounts[to_bank]
                receiver_bank.Balance+=amount
                if medium=="Bank to Bank":    
                    tr=Transactions(date.today(),sender.Bank_Name,sender.Account_No,receiver_bank.Bank_Name,receiver_bank.Account_No,medium,amount)
                elif medium=="Pay via Phone number":
                    receiver=Database.Users[to_user].Phone_No
                    tr=Transactions(date.today(),sender.Bank_Name,self.Phone_No,receiver_bank.Bank_Name,receiver,medium,amount)
                elif medium=="Pay via UPI":
                    tr=Transactions(date.today(),sender.Bank_Name,sender.UPI_ID,receiver_bank.Bank_Name,receiver_bank.UPI_ID,medium,amount)
                elif medium=="Self Transfer":
                    if sender.Bank_Name==receiver_bank.Bank_Name:
                        receiver_bank.Balance-=amount
                        print('\u274e',end=" ")
                        print("Can't Transfer in same Acoount")
                        return

                    else:
                        tr=Transactions(date.today(),sender.Bank_Name,sender.Account_No,receiver_bank.Bank_Name,receiver_bank.Account_No,medium,amount)
                        print('\u2705',end=" ")
                        print("Transaction Successful")
                return tr
            
class GPAY:
    Version='GPay 2023.1'
    App_Name='Google Pay'
    def __init__(self,state):
        self.State=state

    def index(self):
        print("---------------------------------------------")
        print("Welcome to Google Pay.....")
        print("1 - Login")
        print("2 - Signup")
        print("3 - Exit")
        choice=int(input("Enter your choice : "))
        if choice==1:
            self.login()
        elif choice==2:
            self.signup()
        elif choice==3:
            self.back(1)
        else:
            print("Invalid choice")
            self.index()

    def signup(self):
        print("---------------------------------------------")
        name=input("Enter user name : ")
        phone=int(input("Enter Phone number : "))
        email=input("Enter Email id : ")
        password=input("Enter Password : ")
        flag=Database.is_new_user(phone)
        if flag:
            user=User(name,phone,email,password)
            print('\u2705',end=" ")
            print("GPAY account created successfully ")
        else:
            print('\u274e',end=" ")
            print("This Phone number aldready exist ")
        self.index()

    # it is login page for GPAY
    def login(self,ver=1):
        print("---------------------------------------------")
        if ver==1:
            phone=int(input("Enter Phone number: "))
            password=input("Enter Password : ")
            ver=Database.verify(phone,password)
        if ver:
            ver.home()
        else:
            print("1 - Retry")
            print("2 - Forget password")
            print("3 - Back")
            print("4 - Exit")
            choice=int(input("Enter your choice : "))
            if choice==1:
                if ver==2:
                    self.modify_password()    
                else:
                    self.login()
            elif choice==2:
                self.forget_password()
            elif choice==3:
                self.back(2)
            elif choice==4:
                self.back(1)
            else:
                print("Invalid choice ")
                self.login(ver=False)

    def back(self,num):
        print("---------------------------------------------")
        if num==1:
            print("Thank you")
            return False
        elif num==2:
            self.index()
        elif num==3:
            self.home()
        
    def back_or_exit(self):
        print("---------------------------------------------")
        print("1 - Back")
        print("2 - Exit")
        choice=int(input("Enter your choice : "))
        if choice==1:
            self.back(3)
        elif choice==2:
            self.back(1)
        else:
            print("Invalid choice")
            return self.back_or_exit()
        return choice

    def forget_password(self):
        print("---------------------------------------------")
        email=input("Enter your Email id : ")
        flag=Database.valid_email(email)
        if flag:
            print('\u2705',end=" ")
            print("Password changed successfully")
        self.login(ver=False)


    # it is home page for GPAY
    def home(self):
        print("---------------------------------------------")
        print()        
        print("1 - Bank to Bank transfer")
        print("2 - Pay via Phone number")
        print("3 - Pay via UPI ID")
        print("4 - Self Transfer")
        print()
        print("5 - Check balance")
        print("6 - Transaction history")
        print("7 - Profile")
        print("8 - Exit or Logout")
        choice=int(input("Choose your choice : "))
        if choice==1:
            self.bank_transfer_page()
        elif choice==2:
            self.phone_transfer_page()
        elif choice==3:
            self.upi_id_transfer_page()
        elif choice==4:
            self.self_transfer_page()
        elif choice==5:
            self.check_balance_page()
        elif choice==6:
            self.transaction_history_page()
        elif choice==7:
            self.profile_page()
        elif choice==8:
            self.back(1)
        else:
            print("Invalid Choice ")
            self.home()

    def bank_transfer_page(self):
        print("---------------------------------------------")
        to_bank=int(input("Enter Receiver Account number : "))
        amount=float(input("Enter Amount : "))
        temp=self.bank_transfer(to_bank,amount)
        if temp==False:
            print('\u274e',end=" ")
            print("Transaction Unsuccessfull")
        elif temp==True:
            print('\u2705',end=" ")
            print("Transaction Successfull")
        self.back_or_exit()

    def phone_transfer_page(self):
        print("---------------------------------------------")
        to_phone=int(input("Enter Receiver Phone Number : "))
        amount=float(input("Enter Amount : "))
        temp=self.pay_phone_no(to_phone,amount)
        if temp==False:
            print('\u274e',end=" ")
            print("Transaction Unsuccessfull")
        elif temp==True:
            print('\u2705',end=" ")
            print("Transaction Successfull")
        self.back_or_exit()
    

    def upi_id_transfer_page(self):
        print("---------------------------------------------")
        to_upi=input("Enter Receiver UPI id : ")
        amount=float(input("Enter Amount : "))
        temp=self.pay_upi_id(to_upi,amount)
        if temp==False:
            print('\u274e',end=" ")
            print("Transaction Unsuccessfull")
        elif temp==True:
            print('\u2705',end=" ")
            print("Transaction Successfull")
        self.back_or_exit()

    def  self_transfer_page(self):
        print("---------------------------------------------")
        self.show_linked_bank()
        choice=int(input("Choose Receiver Bank: "))
        if choice-1<len(self.Bank_Accounts):
            to_bank=self.Bank_Accounts[choice-1].Bank_Name
            amount=float(input("Enter Amount : "))
            temp=self.self_transfer(to_bank,amount)
            if temp==False:
                print('\u274e',end=" ")
                print("Transaction Unsuccessfull")
            elif temp==True:
                print('\u2705',end=" ")
                print("Transaction Successfull")
        else:
            print("Invalid choice")
        self.back_or_exit()
        
    def check_balance_page(self):
        print("---------------------------------------------")
        self.check_balance()
        self.back_or_exit()


    def transaction_history_page(self):
        print("---------------------------------------------")
        self.show_transactions()
        self.back_or_exit()

    def profile_page(self):
        print("---------------------------------------------")
        self.profile()
        print("1 - Add Bank Account")
        print("2 - Remove Bank Account")
        print("3 - Change Account PIN")
        print("4 - Change password")
        print("5 - back")
        print("6 - Exit")
        choice=int(input("Enter your choice : "))
        if choice==1:
            self.add_bank()
            self.profile_page()
        elif choice==2:
            self.remove_bank()
            self.profile_page()
        elif choice==3:
            self.modify_pin()
            self.profile_page()
        elif choice==4:
            self.modify_password()
            self.profile_page()
        elif choice==5:
            self.back(3)
        elif choice==6:
            self.back(1)
        else:
            print("Invalid Choice")
            self.profile_page()

class User (Database,Bank_Details,Transactions,GPAY):
    
    def __init__(self,name,phone,email,password):
        self.User_Name=name
        self.Phone_No=phone
        self.Email=email
        self.Password=password
        self.Bank_Accounts=[]
        self.Transaction_History=[]
        self.__class__.Users.append(weakref.proxy(self))            

    def profile(self):
        print("User name     : ",self.User_Name)
        print("Phone number  : ",self.Phone_No)
        print("Email ID      : ",self.Email)
        print("Bank Accounts : ")
        index=1
        for i in range(len(self.Bank_Accounts)):
            print(index," - ",self.Bank_Accounts[i].Bank_Name," "*10,self.Bank_Accounts[i].UPI_ID)
            index+=1
        
    def modify_password(self):
        password=input("Enter current Password : ")
        if self.Password==password:
            password=input("Enter new password : ")
            confirm=input("Enter confirm password: ")
            if password==confirm:
                self.Password=password
                print('\u2705',end=" ")
                print("Password Changed Successfully ")
            else:
                print('\u274e',end=" ")
                print("New Password and Confirm Password not matched")
        else:
            print('\u274e',end=" ")
            print("Invalid Password")
            self.login(ver=2)

    # UPI payment method
    def pay_upi_id(self,to_upi,amount):
        user,bank=self.find_upi_id(to_upi)
        medium="Pay via UPI"
        if user!=None:
            tr=self.bank_transfer_process(user,bank,medium,amount)
            if tr==None:
                return
            self.Transaction_History.append(tr)
            Database.Users[user].Transaction_History.append(tr)
            return True
        else:
            print('\u274e',end=" ")
            print("Invalid Account number")
            return False

    # to finding the receiver details thorugh the upi_id
    def find_upi_id(self,to_upi):
        user=None
        bank=None
        for i in range(len(Database.Users)):
            for j in range(len(Database.Users[i].Bank_Accounts)):
                if Database.Users[i].Bank_Accounts[j].UPI_ID==to_upi:
                    user=i
                    bank=j
        return(user,bank)

    # Phone number payment method
    def pay_phone_no(self,to_phone,amount):
        user=self.find_phone_no(to_phone)
        if user!=None:
            bank=0
            medium="Pay via Phone number"
            tr=self.bank_transfer_process(user,bank,medium,amount)
            if tr==None:
                return
            self.Transaction_History.append(tr)
            Database.Users[user].Transaction_History.append(tr)
            return True

    # to finding the receiver details thorugh the Phone number
    def find_phone_no(self,to_phone):
        user=None
        for i in range(len(Database.Users)):
                if Database.Users[i].Phone_No==to_phone:
                    user=i
        return(user)
    
    # Bank to Bank Method
    def bank_transfer(self,to_account,amount):
        user,bank=self.find_account(to_account)
        medium="Bank to Bank"
        if user!=None:
            tr=self.bank_transfer_process(user,bank,medium,amount)
            if tr==None:
                return
            self.Transaction_History.append(tr)
            Database.Users[user].Transaction_History.append(tr)
            return True
        else:
            print('\u274e',end=" ")
            print("Invalid Account number")
            return False

    # to finding the receiver details thorugh the account number
    def find_account(self,to_account):
        user=None
        bank=None
        for i in range(len(Database.Users)):
            for j in range(len(Database.Users[i].Bank_Accounts)):
                if Database.Users[i].Bank_Accounts[j].Account_No==to_account:
                    user=i
                    bank=j
        return(user,bank)

    # self payment method
    def self_transfer(self,bank,amount):
        for i in range (len(self.Bank_Accounts)):
            if self.Bank_Accounts[i].Bank_Name==bank:
                bank=i       
        user,bank=self.find_account(self.Bank_Accounts[bank].Account_No)
        medium="Self Transfer"
        if user!=None:
            tr=self.bank_transfer_process(user,bank,medium,amount)
            if tr==None:
                return False
            self.Transaction_History.append(tr)
            return True
            
    # it show all the transaction history for the user
    def show_transactions(self):
        print("#############################################")
        for i in self.Transaction_History:
            
            print(i.Date,"   ",i.Medium,"  Rs. ",i.Balance)
            print(i.Send_Bank," "*20,i.Receive_Bank)
            print(" "*17,">>>")
            print(i.Sender," "*15,i.Receiver)
            print("---------------------------------------------")



# User creation
#user1=User('Kumaresan',9095379041,'kumua2001@gmail','11111')
#user2=User('Thilagavathi',9876543210,'thilaga2003@gmail','22222')
#user3=User('Sathish',9080706050,'sathish@gmail','33333')

# add bank
#user2.add_bank_direct('IOB','IOB001',1111111111,'thila@iob001','1111',1000)
#user2.add_bank_direct('SBI','SBI001',2222222222,'thila@sbi001','2222',2000)
#user2.add_bank_direct('ICICI Bank','ICICIBE005',3333333333,'thila@icici001','3333',3000)
#user1.add_bank_direct('HDFC Bank','HDFCBD004',4444444444,'kumar@hdfc001','4444',4000)
#user1.add_bank_direct('Axis Bank','AXIBSA001',5555555555,'kumar@axis001','5555',5000)        

# Trasaction method
#user1.bank_transfer(22,100)
#user1.pay_phone_no(9876543210,200)
#user1.pay_upi_id('thila@iob001',300)
#user1.self_transfer('Axis Bank',400)

g=GPAY('Installed')
power=True
while(power):
    power=g.index()

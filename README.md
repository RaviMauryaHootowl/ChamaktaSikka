<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://drive.google.com/uc?export=view&id=15r9iyueR-7fGt418Q_sBCOxwCLzx9sxk" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Chamakta Sikka</h1>
  <p align="center">
    Our own Cryptocurrency
    <br><br>
  </p>
</p>

## 🤔 About Project
Chamakta Sikka is our attempt to create our own Cryptocurrency System from scratch using Blockchains.

## 👨‍💻 Team members
* Member - Ravi Maurya
* Member - Shreyas Penkar
* Member - Nikheel Indanoor
* Member - Arnav Ganatra

## 🙏 Mentors
* Mentor - Aditya Patkar
* Mentor - Archeel Parekh

## 🚀 Instructions to run the application (PRODUCTION)

1. Create a .env file in root directory of the project
```
REACT_APP_MODE=PRODUCTION
```
2. Build the react frontend
```bash
npm run build
```
3. Create a virtual environment for python, activate the virtual environment.

4. Install Python libraries
```bash
pip install -r requirements.txt
```

5. Inside the api/launchapi.txt, change the ports list to number of ports wanted
```python
ports = [5000, 5001]
``` 

6. Launch multiple terminals and run this command on seprate terminals
```bash
cd api
python app.py 5000
```
```bash
cd api
python app.py 5001
```
etc...
<br>

7. Launch one extra terminal and run this command to connect the nodes together
```bash
cd api
python launchapi.py
```
<br>

8. Now in your browser open the ports in different tabs
```
http://localhost:5000/
```
```
http://localhost:5001/
```
etc...
<br>


## 📃 Description
Chamakta Sikka is our attempt to create our own Cryptocurrency System from scratch using Blockchains. The main aim for our project was to learn how Blockchain and Cryptocurrency works, understand the core concepts and then try to create our own system.<br/><br/>

The final product that we have made is a Web Application. Multiple Users running on different local ports would login to the system. Each user will receive a his public and private keys which are generated using RSA. The user can pay amount in csk (our cryptocurrency unit). Paying amount to another user goes into the Mempool. Then at any point of time another user called as the Miner could mine a block. This process takes the transactions from the Mempool and creates and mines a new block into the Blockchain. After this according to the transactions which have been mined in the block, the wallet of each user updates.

Don't forget to replace the link here with **_your own Github repository_** link.

Along with this, add the link of the drive folder that contains the app APK/Screenshots/Screen Recordings. If you have hosted your project on the web, add that link as well.

* GitHub repo link: [https://github.com/Shreyas-Penkar/ChamaktaSikka](https://github.com/Shreyas-Penkar/ChamaktaSikka)
* Drive link: [Drive link here](https://drive.google.com/)

## 🛠 Technology stack

Tools and technologies that you learnt and used in the project.

1. Frontend - Javascript, ReactJS
2. Backend - Python
3. APIs - Flask
4. SocketIO


## 🧠 Applications
>How can your project do its part in solving a real-life problem? What are its possible applications? Decribe here.

## 👨‍🎓 What did we learn from this project
Here are things we learned during Skill Up 2.0

1. Ravi Maurya - <br/>
It had been an amazing journey working on this project. The main core of this project is based on Blockchains, so I got to learn Blockchains in deep. We tried to implement everything on our own as we wanted to learn the fundamentals of Blockchain, this means too many bugs and errors, which also means so much to learn from it.
2. Member 2 name - Description
3. Member 2 name - Description
4. Member 2 name - Description

## 🔮 Future scope
Here are few things that we want to add in future<br/>
- [ ] Increasing Security
- [ ] Mobile App
- [ ] GPU Support for Mining

## 🎨 Screenshots

![Screenshot alt text](https://drive.google.com/uc?export=view&id=1SzwPcVRC2KqfNYQcmmLANMXCOuMYM5L-)
![Screenshot alt text](https://drive.google.com/uc?export=view&id=1I2E_upOicKHDDouSHRQzGKHw4CWSXRU-)
![Screenshot alt text](https://drive.google.com/uc?export=view&id=1OMBBAl3nXhHpwFuXDS6xIsE1XbrMMGbh)
![Screenshot alt text](https://drive.google.com/uc?export=view&id=1225zHGSl7CVypaINeRjsmHH5ZOzCyDNG)

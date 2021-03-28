import React, {useState, useEffect} from 'react';
import styles from './Home.module.css';
import axios from 'axios';
import {useLocation} from 'react-router-dom';
import io from 'socket.io-client';
const socket = io.connect('/');
const Home = () => {
  const location = useLocation();
  
  const [user, setUser] = useState(null);
  const [allUsers, setAllUsers] = useState([]);

  const [payToId, setPayToId] = useState("");
  const [payAmount, setPayAmount] = useState(0);

  const userColorArray = [
    {start: '#F33030', end: '#F47272'},
    {start: '#30F27E', end: '#70F37D'},
    {start: '#3097F6', end: '#69ACEA'},
    {start: '#BB29FF', end: '#D67EF4'},
    {start: '#FFB629', end: '#FFB629'}
  ]

  useEffect(() => {
    const userToCreate = location.state;
    socket.emit("addNewUser", userToCreate);
  }, [location])

  useEffect(() => {

      // Getting the user info for first time only
      socket.on("userInfo", data => {
        // console.log(data);
        setUser(data);
      });

      // Getting list of all users when there is any update
      socket.on("userRefresh", data => {
        // console.log(data);
        setAllUsers(data);
      });

      // If user exits the website, to disconnect him/her
      return () => {
        socket.close()
      }
  }, [])

  return (
    <div className={styles.homePage}>
      <div className={styles.homeNavContainer}>
        <span className={styles.header}>Chamakta Sikka</span>
        <span className={styles.subHeader}>Our Own Cryptocurrency</span>
      </div>
      <div className={styles.homePagePortalContainer}>
        <div className={styles.usersOnlineContainer}>
          <span className={styles.usersOnlineHeader}>Users Online</span>
          <div className={styles.usersOnlineListContainer}>
            {
              allUsers.map((thisUser, index) => {
                return (
                  <div className={styles.userAvatar} style={{backgroundImage : `linear-gradient(145deg, ${userColorArray[index % userColorArray.length].start}, ${userColorArray[index % userColorArray.length].end})`}}>
                    {thisUser.username}
                  </div>
                );
              })
            }
          </div>
        </div>

        <div className={styles.payAndAccountContainer}>
          <div className={styles.payOuterContainer}>
            <span className={styles.payHeader}>Pay Someone</span>
            <div className={styles.payInnerContainer}>
              <div className={styles.payForm}>
                <span className={styles.inputLabel}>To</span>
                <input className={styles.payToInput} value={payToId} onChange={(e) => {setPayToId(e.target.value)}} type="text"/>
                <span className={styles.inputLabel}>Amount</span>
                <input className={styles.payAmountInput} value={payAmount} onChange={(e) => {setPayAmount(e.target.value)}} type="number"/>
                <button className={styles.payBtn}>PAY</button>
              </div>
            </div>
          </div>

          <div className={styles.accountOuterContainer}>
            <span className={styles.accountHeader}>Your Account</span>
            <div className={styles.accountCardContainer}>
              <div className={styles.walletContainer}>
                <span className={styles.walletHeader}>{(user != null) ? user.username : ""}'s Wallet</span>
                <div className={styles.walletValueContainer}>
                  <span className={styles.walletValue}>{(user != null) ? user.wallet_balance : ""}</span>
                  <span className={styles.walletValueUnit}>csk</span>
                </div>
              </div>
              <div className={styles.accountNumberContainer}>
                <span className={styles.accountNumberHeader}>Account Number</span>
                <span className={styles.accountNumberValue}>{ ( user != null) ? user.uuid : 0}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
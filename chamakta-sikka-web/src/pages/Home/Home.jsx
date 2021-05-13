import React, {useState, useEffect} from 'react';
import styles from './Home.module.css';
import axios from 'axios';
import {useLocation} from 'react-router-dom';
import io from 'socket.io-client';
console.log(window.location.href);
const port = parseInt((window.location.href).split(':')[2].substr(0,4))
console.log(port+2000)
const socket = io.connect(`http://localhost:${port+2000}/`);
const Home = () => {
  const location = useLocation();
  
  const [user, setUser] = useState(null);
  const [allUsers, setAllUsers] = useState([]);

  const [payToId, setPayToId] = useState("");
  const [payAmount, setPayAmount] = useState(0);
  const [payIncentive, setPayIncentive] = useState(0);
  const [isInfoCardVisible, setIsInfoCardVisible] = useState(false);
  const [userToDisplayInfoCard, setUserToDisplayInfoCard] = useState(null);

  const [memPool, setMemPool] = useState(["A", "B", "C", "D", "E", "F", "G", "H", "I"]);

  const toggleInfoCardVisibility = () => {
    setIsInfoCardVisible(!isInfoCardVisible);
  }

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
      <UserInfoCard userToDisplayInfoCard={userToDisplayInfoCard} isInfoCardVisible={isInfoCardVisible} setIsInfoCardVisible={setIsInfoCardVisible} />
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
                return <UserAvatar user={thisUser} index={index} setUserToDisplayInfoCard={setUserToDisplayInfoCard} toggleInfoCardVisibility={toggleInfoCardVisibility} />
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
                <span className={styles.inputLabel}>Incentive</span>
                <input className={styles.payAmountInput} value={payIncentive} onChange={(e) => {setPayIncentive(e.target.value)}} type="number"/>
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
        <div className={styles.mempoolBoxContainer}>
          <div className={styles.mempoolOuterContainer}>
            <div className={styles.mempoolHeaderContainer}>
              <span className={styles.mempoolHeader}>Mempool</span>
              <button className={styles.mineBtn}>MINE</button>
            </div>
            
            <div className={styles.mempoolInnerContainer}>
              {
                memPool.map((transaction) => {
                  return <MempoolTransactionCard />
                })
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const UserAvatar = ({user, index, toggleInfoCardVisibility, setUserToDisplayInfoCard}) => {
  
  const userColorArray = [
    {start: '#F33030', end: '#F47272'},
    {start: '#30F27E', end: '#70F37D'},
    {start: '#3097F6', end: '#69ACEA'},
    {start: '#BB29FF', end: '#D67EF4'},
    {start: '#FFB629', end: '#FFB629'}
  ]

  const onUserAvatarClick = () => {
    setUserToDisplayInfoCard(user);
    toggleInfoCardVisibility();
  }


  return (
    <div onClick={onUserAvatarClick} className={styles.userAvatar} style={{backgroundImage : `linear-gradient(145deg, ${userColorArray[index % userColorArray.length].start}, ${userColorArray[index % userColorArray.length].end})`}}>
      
    </div>
  );
}

const UserInfoCard = ({userToDisplayInfoCard, isInfoCardVisible, setIsInfoCardVisible}) => {


  return (
    <>{(isInfoCardVisible) && 
      <div className={styles.userInfoCardBackground}>
        <div className={styles.userInfoContainer}>
          <div className={styles.infoTitle}>Account No: </div>
          <span className={styles.infoValue}>{userToDisplayInfoCard.uuid}</span>
          <span className={styles.infoTitle}>Name: </span>
          <span className={styles.infoValue}>{userToDisplayInfoCard.username}</span>
          <button onClick={() => {setIsInfoCardVisible(false)}}>close</button>
        </div>
      </div>
    }</>
  );
}

const MempoolTransactionCard = () => {
  return (
    <div className={styles.mempoolTransactionCardContainer}>
      <div className={styles.transactionCard}>
        <span className={styles.transactionCardHeader}>Transaction Hash</span>
        <span className={styles.transactionCardValue}>a35wva1we35va3f15weaf4we33</span>
        <span className={styles.transactionCardHeader}>Sender</span>
        <span className={styles.transactionCardValue}>a4v6e8w4va664ag3awf5we1f3wa</span>
        <span className={styles.transactionCardHeader}>Reciever</span>
        <span className={styles.transactionCardValue}>ser4b364a6w4a6g4a6w8g4a6r8g</span>
        <span className={styles.transactionCardHeader}>Timestamp</span>
        <span className={styles.transactionCardValue}>8:03 PM, 31/03/2021</span>
      </div>
    </div>
  );
}

export default Home;
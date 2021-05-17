import React, {useState, useEffect} from 'react';
import styles from './Login.module.css';
import axios from 'axios';
import {useHistory} from 'react-router-dom';

const Login = () => {
  const history = useHistory();
  const [userName, setUserName] = useState("");
  const [initAmount, setInitAmount] = useState("");

  const loginUser = () => {
    console.log(userName);
    // axios.post('/addnewuser', {
    //   'username' : userName,
    //   'initamount' : initAmount
    // }).then((res) => {
    //   const userCreated = res.data;
    //   if(userCreated.uuid && userCreated.uuid.length > 0){
    //     // user Created successfully
    //     history.push("/home", userCreated);
    //   }
    // }).catch((err) => {
    //    console.log(err);
    // })

    history.push("/home", {
      'username' : userName,
      'initamount' : initAmount
    })

  }

  return (
    <div className={styles.loginPage}>
      <div className={styles.loginNavContainer}>
        <span className={styles.header}>Chamakta Sikka</span>
        <span className={styles.subHeader}>Our Own Cryptocurrency</span>
      </div>
      <div className={styles.loginContainer}>
        <div className={styles.loginForm}>
          <span className={styles.inputLabel}>Username</span>
          <input className={styles.nameInput} value={userName} onChange={(e) => {setUserName(e.target.value)}} type="text" name="name" id=""/>
          <span className={styles.inputLabel}>Initial Amount</span>
          <input className={styles.initMoney} value={initAmount} onChange={(e) => {setInitAmount(e.target.value)}} type="number" name="money" id=""/>
          <button className={styles.enterBtn} onClick={loginUser}>JOIN</button>
        </div>
      </div>
    </div>
  );
}

export default Login;
import React, {useState, useEffect} from 'react';
import styles from './Login.module.css';
import axios from 'axios';
import {useHistory} from 'react-router-dom';
import Loader from '../../components/Loader/Loader';
const port = parseInt((window.location.href).split(':')[2].substr(0,4));
const baseAddress = `http://localhost:${port+2000}`;


const Login = () => {
  const history = useHistory();
  const [userName, setUserName] = useState("");
  const [initAmount, setInitAmount] = useState("");
  const [isDoingCoinBaseTransaction, setIsDoingCoinBaseTransaction] = useState(false);

  const loginUser = () => {
    setIsDoingCoinBaseTransaction(true);
    axios.post(`${baseAddress}/api/coin_base_transaction`, {
      "amount": parseInt(initAmount)
    }).then((res) => {
      history.push("/home", {
        'username' : userName,
        'initamount' : initAmount
      })
    })
    .catch((e) => {
      alert("Server Error")
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
          <button className={styles.enterBtn} onClick={loginUser}>
            {(isDoingCoinBaseTransaction) ? <Loader size={20} border={3} color={"#ffffff"}/> : "JOIN"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
import React from "react";
import styles from './CustomInput.module.sass'

export default function CustomInput(props) {
    return(
        <div className={styles.input}>
            <input placeholder={props.text} type={props.type ? props.type : "text"}/>
        </div>
    )
}
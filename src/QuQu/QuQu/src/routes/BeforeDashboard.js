import { useLocation, useNavigate } from 'react-router-dom'
import React, { useEffect, useState, useCallback, useRef } from "react";
import axios from 'axios'
import Button from 'react-bootstrap/Button';
import shoes from '../servers/data.js';
import server from '../servers/data.js'
import local from '../servers/data.js'

export default function BeforeDashboard(props){
    let origin = ''
    if (window.navigator.userAgent.indexOf('Mac') > 0){
        origin = local['local']
    } else if (window.navigator.userAgent.indexOf('Linux') > 0){
        origin = server['server']
    }
    const state = useLocation();
    let localhost = origin + 'api'
    let navigate = useNavigate()

    return (
        <>
            <div className='custom-btn content-start-button'>
              <Button onClick={(e)=>{ 
                //api/ds
                let url = localhost + '/ds'
                let form = new FormData()
                form.append('user_name', JSON.stringify(window.user))
                axios.post(url , form
                  ).then(async(res)=>{
                    navigate('/design-improvement',{
                      state: {
                        cluster : res.data,     
                    }
                    })

                  }).catch((err)=>{
                })

                // navigate(nextPage[props.location.pathname],{
                //   state: window.ys
                  
                // })
                
                }} size='lg'>Next</Button></div>
        </>
    )
  }
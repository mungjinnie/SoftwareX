import React, { useEffect, useState, useCallback } from "react";

function MenuStart(props){

    return (
      <div className='user-name'>
        <div className='menu-container' style={{ visibility : 'hidden'}}  >
          <div>
            {
              props.setSelectedYs((selectedYs) => '23FW')
            } 
          {
            props.seasons.map((e, i) => {
              return <div className='menu-row'>
                {
                  props.years.map((ee, ii) => {
                    return (
                      <div className='menu-column' onClick={()=>{
                        
                        //Initial color settings
                        props.seasons.map((e, i) => {
                          props.years.map((ee, ii) => {
                            let name = ee+e;
                            props.ys[name] = 'rgb(196 198 251)'
                            props.ChangeYSColor((ys) => ys)
                          })
                        }, [])

                        e = 'FW'
                        ee = '23'
                        
                        //Set to last clicked color
                        let name = ee+e;
                        props.ys[name] = 'rgb(97 106 120)'
                        let copy = {...props.ys}
                        props.ChangeYSColor((ys) => copy)

                        let tmp = ee+e;
                        window.ys = '23FW'
                        window.season = e 
                        // props.setSelectedYs((selectedYs) => tmp)
                        props.setSelectedYs((selectedYs) => tmp)
                      }}
                      style={{
                        backgroundColor: props.ys[ee+e] === 'rgb(97 106 120)'? 'rgb(97 106 120)' : 'rgb(196 198 251)',
                      }} 
                      disabled={ ee === 23 ? true : false }
                      > { 
                          ee+e
                        }</div>
                    )
                  })
                }
              </div> 
            })
          }
          </div>
        </div>
      </div>
    )
  }
  export default MenuStart;
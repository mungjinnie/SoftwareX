import { useLocation } from 'react-router-dom'
import React, { useEffect, useState, useCallback, useRef } from "react";
import CustomClusterImages2 from '../CustomClusterImages2.js';
import shoes2 from '../servers/data.js';

export default function Naming(props){
    const state = useLocation();

    let [showNaming, setShowNaming] = useState(false);
    let [inputValue, setInputValue] = useState(null);
    let [selectedStyle, setSelectedStyle] = useState('Style0')

    const autoNaming = (e) =>{
        let tmp = {...e};
        let i = 0
        let new_style = []
        for (i; i < Object.keys(tmp).length;i++) {
            new_style.push('Style'+ i.toString())
        }
        let old_key = []
        Object.keys(tmp).map((style2)=>{
            var index = Object.keys(tmp).indexOf(style2)
            old_key.push(style2)
            Object.defineProperty(tmp, new_style[index],
                Object.getOwnPropertyDescriptor(tmp, style2));
        })

        let j = 0
        for (j; j < old_key.length;j++) {
            delete tmp[old_key[j]]
        }
        
        props.setNaming(tmp)
        setSelectedStyle('Style0')

    }

    const handleConfirm =    (e) => {

        if (inputValue === ''){
            return ;
        }

        let tmp = {...props.naming};
        let oldKey = Object.keys(tmp).find(key => tmp[key]['status'] === true);
        let sanityCheck = Object.keys(tmp).find(key => key === inputValue);

        if (sanityCheck !== undefined){
            return ;
        }

        // log
        props.setConfirmTC(props.confirmTC + 1)

        //naming by its input
        if (inputValue !== "" && inputValue !== null && sanityCheck === undefined){
            Object.defineProperty(tmp, inputValue,
                Object.getOwnPropertyDescriptor(tmp, oldKey));
            delete tmp[oldKey];
        }
        props.setNaming(tmp)
        setSelectedStyle(inputValue)
    };

    const updateInput = (e) => {
        setInputValue(e.target.value)   
    }

    useEffect( () => {
        let initial ={}
        initializeNaming(initial) 
        props.setNaming(initial)
        // autoNaming(props.naming)
        // autoNaming(props.naming)
        autoNaming(initial)

    }, []);

    useEffect( () => {
        
    }, [selectedStyle]);

    const initializeNaming = (initial) => {
        Object.keys(state.state['cluster']).forEach((style, i) => {
            if (i === 0 ){
                setSelectedStyle(style)
            }
            // What k value is k?
            initial[style] = {}
            initial[style]['images'] = []
            initial[style]['images'] = state.state['cluster'][style]['images']
            initial[style]['old_name'] = style
            if ( i === 0) {
                initial[style]['status'] = true
            } else {
                initial[style]['status'] = false
            }  
        })
    }



    return (
        <div>
            <div className='cluster-container' style={{ display : props.freeLevel === 0  ? 'none' : 'block'}}>
             <div className='current-attr-title cluster-mix-stack'>
                <p className='current-attr-label'>Final style: </p>
                {
                    Object.keys(props.naming).map((style, i) => {
                        return (
                            
                            <> 
                                <div className= {`${props.naming[style]['status'] === false ? 'btn': 'btn btn-dark'} cluster-selected-stack-inside btn`}
                                    onClick={(ee)=>{
                                        // setShowNaming(true);
                                        let tmp = {...props.naming};
                                        Object.keys(tmp).map((style2)=>{
                                            Object.keys(tmp[style2]).map(()=>{
                                                tmp[style2]['status'] = false
                                            })
                                        })

                                        tmp[style]['status'] = true;
                                        props.setNaming(tmp);
                                        setSelectedStyle(style)
                                }}> { style !== 'log' ? style : ''}</div>           
                            </>                         
                        );
                    })
                }
                <div className='current-attr-title cluster-mix-stack' style={{ display : 'none'}}> 

                    <div className='cluster-mix'>
                        <input className='input-naming' placeholder="Please name the style"
                            onChange={(e)=>{
                                updateInput(e)
                            }}
                        />
                    </div>
                    <div className='btn cluster-mix'
                        onClick={(e)=>{
                            handleConfirm(e)
                        }}
                    >Confirm</div>
                </div>
            </div>
            <div className='naming-images-box'>
                <CustomClusterImages2 setNaming={props.setNaming} naming={props.naming} style={selectedStyle} type={'naming'}/>
            </div>
        </div>
    </div>
    )
  }
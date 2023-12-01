import { useLocation } from 'react-router-dom' 
import React, { useEffect, useState, useCallback, useRef } from "react";
import shoes2 from '../servers/data.js';
import { alpha, styled } from '@mui/material/styles';
import CustomSlider from '../CustomSlider.js'
import CustomClusterImages from '../CustomClusterImages';
import LazyLoad from 'react-lazyload';

const ListItem = styled('li')(({ theme }) => ({
    margin: theme.spacing(0.5),
  }));

export default function Cluster(props){
    const state = useLocation();

    let alphabet ='k'
    if (props.method === 'GMM'){
        alphabet = 'g'
    }

    let [height, setHeight] = useState(700)
    let ref = useRef(null);

    useEffect( () => {
        props.setMethod('K-means');
        props.setClusterNum(props.freeLevel > 0? 20 :15);
         
        //If the degree of freedom is 0, all are selected.
        let initial ={}
        initializeCluster(initial, 'clusterValue') 
        props.setCluster(initial)

        let initial2 ={}
        initializeCluster(initial2, 'clusterShow')  
        setClusterShow(initial2)
    }, [props.freeLevel]);

    useEffect( () => {
        let initial2 ={}
        initializeCluster(initial2, 'clusterShow')  
        setClusterShow(initial2)
    }, [props.clusterNum]);

    useEffect( () => {
        let initial2 ={}
        initializeCluster(initial2, 'clusterShow')  
        setClusterShow(initial2)
    }, [props.method]);

    useEffect( () => {
        let initial ={}
        initializeCluster(initial, 'clusterValue') 
        props.setCluster(initial)

        let initial2 ={}
        initializeCluster(initial2, 'clusterShow')  
        setClusterShow(initial2)
    }, []);

    const handleDelete = (k, cluster_x, m) => {
        let copyCluster = {...props.cluster}
        copyCluster[m][k][cluster_x]['status'] = !copyCluster[m][k][cluster_x]['status']
        props.setCluster(copyCluster)
        props.setClusterCount(props.clusterCount - 1)
    };

    const handleSliderChange = (event, newValue) => {
        // If you change the number
        props.setClusterNum(newValue);    
        props.setClusterNumTC(props.clusterNumTC +1)   
        // Get the right results
    };

    const initializeCluster = (initial, type) => {      
        let first = ''
        //If there are no degrees of freedom, K-means is default.
        Object.keys(state.state['cluster']).forEach((m, mi) => {
            initial[m] = {}
            Object.keys(state.state['cluster'][m]['clusters']).forEach((k, ki) => {
                // What k value is k?
                initial[m][k] = {}
                Object.keys(state.state['cluster'][m]['clusters'][k]).forEach((element, i) => {
                    //element cluster0
                    initial[m][k][element] = {}
                    Object.keys(state.state['cluster'][m]['clusters'][k][element]).forEach((ee, ii)=>{
                        initial[m][k][element]['status'] = {}
                        
                        //When the degree of freedom is 0, only k15 items are selected.
                        if (props.freeLevel === 0 && k === (props.freeLevel > 0?'k20':'k15')){
                            initial[m][k][element]['status'] = true
                        } else {
                            initial[m][k][element]['status'] = false  
                        }
                        initial[m][k][element]['image'] = {}
                        state.state['cluster'][m]['clusters'][k][element]['image'].map((eee, iii) => {
                            initial[m][k][element]['image'][eee] = true 
                        })
                        
                    })
                })
            })
        })
        first = Object.keys(initial[props.method][alphabet+props.clusterNum])[0]

        if (type==='clusterShow'){
            initial[props.method][alphabet+props.clusterNum][first]['status'] = true
        }
    }

    const [position, setPosition] = useState({ x: 0, y: 0 }); // Position value of box
    // Sets the updated value

    let [clusterShow, setClusterShow] = useState({
        'K-means': {
            [`k${props.clusterNum}`] : {
                'cluster0' : {
                    'status': false,
                    'image': {
                        '123':false
                    },
                }
            }
        },
        'GMM': {
            [`k${props.clusterNum}`] : {
                'cluster0' : {
                    'status': false,
                    'image': {
                        '123':false
                    },
                }
            }
            
        }
    });
    const [clientPos, setClientPos] = useState({ x: 0, y: 0 }); // Value that updates e.client, which is the real-time cursor position
    function dragEnter(e){
        if(!e.clientX || !e.clientY) {
            return false;
        }
    }

    let tmp_alphabet = alphabet
    return (
        <>
            <div className='cluster-container'>
                <ClusterFreeLevel setSelectTC={props.setSelectTC} selectTC={props.selectTC} setClusterCount={props.setClusterCount} clusterCount={props.clusterCount} alphabet={alphabet} method={props.method} setMethod={props.setMethod}  setClusterNum={props.setClusterNum} clusterNum={props.clusterNum} setCluster={props.setCluster} cluster={props.cluster} clusterShow={clusterShow} freeLevel={props.freeLevel} handleDelete={handleDelete} handleSliderChange={handleSliderChange}/>
                <div className='cluster-body'>
                    <div className='cluster-select-left'>
                        <div className='cluster-left' style={{height: height}}>  
                        <div className='cluster-flex-item'>
                        {
                            Object.keys(clusterShow[props.method][alphabet+props.clusterNum]).map((ee, i) => {
                                return (    
                                
                                    <div className={
                                        props.freeLevel > 0 ?[clusterShow[props.method][alphabet+props.clusterNum][ee]['status'] 
                                            && 'btn-dark', 'btn', 'btn btn-y', 'cluster-left-btn'].filter(e=>(!!e)).join(' ')
                                        : clusterShow[props.method][alphabet+props.clusterNum][ee]['status'] === true ? 'btn-dark btn btn-y cluster-left-btn' : 'btn  btn-y cluster-left-btn'
                                        }
                                        style={{ paddingTop:  props.freeLevel  === 0 ? 10 : 0}}
                                        draggable
                                        onDragEnd={(e) =>{
                                            // drop(e)
                                        }}
                                        onDrag={(e)=>{
                                            // dragEnter(e)
                                        }}

                                        onClick={()=>{
                                            let copyClusterShow = {...clusterShow}                                            
                                            Object.keys(copyClusterShow[props.method][alphabet+props.clusterNum]).forEach(v => 
                                                copyClusterShow[props.method][alphabet+props.clusterNum][v]['status'] = false)
                                            copyClusterShow[props.method][alphabet+props.clusterNum][ee]['status'] = true;
                                            setClusterShow(copyClusterShow)
                                            props.setClusterTC(props.clusterTC + 1)
                                        }}>
                                            
                                        {
                                            props.freeLevel  === 0
                                            ?  ee : 'Style'+ee.replace("cluster", "")
                                        }
                                    </div>                    
                                );
                                
                            })
                        }
                        </div>
                    </div>
                    </div>
                    <LazyLoad>
                        <div className='cluster-right' ref={ref}>
                            <CustomClusterImages xClickTC={props.xClickTC} setXClickTC={props.setXClickTC} setXUnclickTC={props.setXUnclickTC} xUnclickTC={props.xUnclickTC} freeLevel={props.freeLevel}  method={props.method} setCluster={props.setCluster} clusterShow={clusterShow} clusterNum={props.clusterNum} type={'cluster'} e={Object.keys(props.cluster)[0]} setClusterShow={setClusterShow}  category={props.cluster} class={'cluster-hover'} params='shoes2' shoes={shoes2}/>                                
                        </div> 
                    </LazyLoad>  
                </div>
            </div>
        </>
    )
  }

  function ClusterFreeLevel(props){ 
    let all_methods = ['K-means', 'GMM']
    let tmp_e = ''
    let tmp_ee = ''
    return (
          <>
            <div className='current-attr-title cluster-selected-stack'>
                <p className='current-attr-label'> Selected style: </p>
                {   
                    // selected cluster
                    // Only those whose key=>value value is true are displayed as chips.
                    all_methods.map((m, mi) => {
                        return (Object.keys(props.cluster[m]).map((e, i) => {
                            //e k5
                            return (
                                <>
                                {
                                    Object.keys(props.cluster[m][e]).map((ee, ii)=>{
                                        tmp_e = e
                                        tmp_e = tmp_e.replace('k20', 'Style')
                                        let ee2 = ee.replace('cluster', '')

                                        return (
                                            <>
                                            {
                                                props.cluster[m][e][ee]['status'] === true?
                                                    <button className=' cluster-selected-stack-inside btn btn-dark' disabled={ props.freeLevel === 0 ? true : false }  onClick={() =>{
                                                        props.handleDelete(e, ee, m)
                                                     }
                                                    }> 
                                                        { 
                                                            props.freeLevel > 0 ?
                                                            tmp_e+ee2
                                                            : ee
                                                        }
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-x" viewBox="0 0 16 16">
                                                            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                                                        </svg>
                                                    </button>
                                                : undefined
                                            }
                                            </>
                                        )
                                         
                                    })
                                    
                                }
                                </>                         
                            );
                            
                        })
                        )
                    })
                }
            </div> 
            <div className='current-attr-title cluster-number-stack' style={{ display : props.freeLevel === 1 ? 'none' : 'none'}}>
                <div className='cluster-number'> </div>
                    <CustomSlider
                        aria-label="Volume"
                        defaultValue={props.freeLevel > 0 ?20 : 15} 
                        step={5}
                        min={10}
                        max={20}
                        onChange={props.handleSliderChange}
                        value={props.clusterNum}
                    />
                <div className='cluster-number' style={{marginLeft: 10}}>{props.clusterNum}</div>
            </div>
            <div className='cluster-select-container'>
                    <div className='btn btn-y cluster-select-btn'
                        style={{display : props.freeLevel === 0 ? 'none' : 'block'}}
                        onClick={()=>{
                            let copyClusterShow = {...props.clusterShow}
                            let copyCluster = {...props.cluster}
                            var filtered = Object.keys(copyClusterShow[props.method][props.alphabet+props.clusterNum]).filter(function(key) {
                                if (copyClusterShow[props.method][props.alphabet+props.clusterNum][key]['status'] === true){
                                    return copyClusterShow[props.method][props.alphabet+props.clusterNum][key]
                                }
                            });
                            copyCluster[props.method][props.alphabet+props.clusterNum][filtered]['status'] = true
                            props.setCluster(copyCluster) 
                            let tmp = props.clusterCount + 1
                            props.setClusterCount(tmp)
                            props.setSelectTC(props.selectTC+1)
                        }}>Select
                    </div>
            </div>
          </>
      )
  }

  

import React, { useEffect, useState } from "react";
import LazyLoad from 'react-lazyload';

//cluster-images
function CustomClusterImages(props) {
    let [arr, setArr] = useState([])
    let emptyArr = [];
    let tmp4 = [];
    useEffect(()=>{
        setArr(emptyArr);
    }, [])

    let alphabet = 'k'
    if (props.method === 'GMM') {
        alphabet = 'g'
    }

    let tmp = [];
    let imageArr = props.type === 'cluster' ? props.clusterShow[props.method][alphabet+props.clusterNum] : props.category[props.e]
    // let prefix_src = props.type === 'cluster' ? 'https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/fw_2023/' : './assets/'+props.e + '/' 
    let prefix_src = 'https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/fw_2023/'

    return (
        
        Object.keys(imageArr)
            .filter((k,v)=>{  
                return props.type === 'cluster' 
                ?   imageArr[k]['status'] === true ?  true :  false
                :   true
            })
            .map((k, v)=>{
            return (
                <>
                {
                    Object.keys(imageArr[k]['image']).map((kk, vv)=>{
                        let test = prefix_src.toString() + kk.toString()
                        return (
                            <div className='lazy-class'>
                            <LazyLoad key={vv} once>
                            <div key={vv} className={'cluster-images-box'}>
                                <div className={'cluster-images'} 
                                    onMouseOver ={
                                        (e) => {
                                           // x 
                                            tmp = [...arr];
                                            tmp = tmp.map((ee, ii)=>{
                                                return false
                                            })
                                            setArr(tmp)
                                            
                                            tmp[vv] = true
                                            setArr(tmp);
                                        }
                                    } 
                                    onMouseOut={
                                        (e) => {
                                            // x 
                                            tmp = [...arr];
                                            tmp[vv] = false;
                                            setArr(tmp);
                                    }}
                                    
                                    onClick={
                                        (e) =>{

                                            if (props.freeLevel > 0){
                                                let tmp2 = {...props.category}
                                                props.type === 'cluster' 
                                                ? tmp2[props.method][alphabet+props.clusterNum][k]['image'][kk] = !tmp2[props.method][alphabet+props.clusterNum][k]['image'][kk]
                                                : console.log('')
                                                props.setCluster(tmp2)

                                                // log
                                                if (tmp2[props.method][alphabet+props.clusterNum][k]['image'][kk] === true){
                                                    props.setXUnclickTC(props.xUnclickTC + 1)
                                                } else {
                                                    props.setXClickTC(props.xClickTC +1)
                                                }

                                            }
                                        }
                                    }
                                    >
    
                                    {   
                                        props.type === 'cluster' 
                                        ?   props.freeLevel > 0 && props.category[props.method][alphabet+props.clusterNum][k]['image'][kk] === false 
                                            ? <img referrerPolicy='no-referrer' style={{opacity:0.1}} src={test} alt={`Image ${vv}`}/>
                                            : <img referrerPolicy='no-referrer' src={test} alt={`Image ${vv}`}/>
                                        : <img referrerPolicy='no-referrer' src={test} alt={`Image ${vv}`}/>
                                    }
                                        
                                    </div>
                                    {
                                        arr[vv] === true && props.freeLevel > 0
                                        ? 
                                            <div className='cluster-hover-text'>
                                                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" className="bi bi-x">
                                                  <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                                                </svg>
                                            </div> 
                                        : 
                                        <div className='cluster-hover-text'></div>
                                    }    
                            </div>
                            </LazyLoad> 
                        </div>
                        )
                    })
                }
                </>
            )
        })          
    )
}
export default  CustomClusterImages;
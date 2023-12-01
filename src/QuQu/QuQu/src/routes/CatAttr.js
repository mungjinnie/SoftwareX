import { useLocation, useNavigate} from 'react-router-dom'
import React, { useEffect, useState, useCallback } from "react";
import shoes from '../servers/data.js';
import server from '../servers/data.js'
import local from '../servers/data.js'
import CustomModal from '../CustomModal';
import CustomClusterImages2 from '../CustomClusterImages2';
import LazyLoad from 'react-lazyload';
import axios from 'axios'

export default function CatAttr(props){ 
    let origin = ''
    if (window.navigator.userAgent.indexOf('Mac') > 0){
        origin = local['local']
    } else if (window.navigator.userAgent.indexOf('Linux') > 0){
        origin = server['server']    
    }
    let count = 0;
    const state = useLocation();
    const navigate = useNavigate();
    let [showCategory, setShowCategory] = useState(true)
    let [brands, setBrands] = useState([]) 
    let [selectedBradn, setSelectedBrand] = useState('')
    let [commonAttr, setCommonAttr] = useState({
        'common_attribute':{
            'Shirt1' :{
                'status': false,
              },
            'Shirt2'  :{
                'status': false,
              },
            'Shirt3' :{
                'status': false,
              },
            'Shirt4' :{
                'status': false,
              },
            'Shirt5' :{
                'status': false,
              },
            'v-neck' :{
                'status': false,
              },
            'Shirt6' :{
                'status': false,
              },
            'Shirt7' :{
                'status': false,
              },
        }
    });
    let tmp = {} 
    let btnClassName = 'btn-attr btn';

    useEffect(()=>{
        // common attribute initialize
        let news = state.state['common_attributes'].forEach(element => {
            let els = element['attributes']
            els = els.split('|')
            tmp['common_attribute'] = {}
            
            els.forEach(ee => {
                tmp['common_attribute'][ee] = {}
                tmp['common_attribute'][ee]['status'] = false  
            });
        })
        setCommonAttr(tmp)

        //hue, tone initialize
        let initial = {}
        let imageInfo = {}
        initializeCategory(initial, props.freeLevel, state.state['cat_attr']);
        props.setCategory(initial);

        let initial2 = {}
        initializeColor2(initial2, props.freeLevel);
        let tmp2 = {...initial2}
        props.setColor(tmp2)
    }, []) 

    useEffect(()=>{
        // common attribute initialize
        let news = state.state['common_attributes'].forEach(element => {
            let els = element['attributes']
            els = els.split('|')
            tmp['common_attribute'] = {}
            
            els.forEach(ee => {
                tmp['common_attribute'][ee] = {}

                if (props.freeLevel === 0){
                    tmp['common_attribute'][ee]['status'] = true 
                } else {
                    tmp['common_attribute'][ee]['status'] = false
                }
                 
            });
        })
        setCommonAttr(tmp)

        //category initialize
        let initial = {}
        initializeCategory(initial, props.freeLevel, state.state['cat_attr']);
        props.setCategory(initial);

        //color initialize
        let initial2 = {}
        initializeColor2(initial2, props.freeLevel);
        props.setColor(initial2)

        let initial4 = state.state['cluster']['brand'].split('|').sort()
        setBrands(initial4)

    }, [props.freeLevel])

    const handleShowCategory = (e, ee) =>{
        props.category[e][ee]['free'] > props.freeLevel ? setShowCategory(false) : setShowCategory(true)
    }

    let attribute_cnt =0 
    Object.keys(props.category).map((e, i)=>{
        Object.keys(props.category[e]).map((ee, ii)=>{
            attribute_cnt += 1
        })
    })

    Object.keys(props.color).map((e, i)=>{
        Object.keys(props.color[e]).map((ee, ii)=>{

            attribute_cnt += 1
        })
    })

    const initializeCategory = (initial, freeLevel, object) => {
        object['category'].forEach((element, i) => {
            let each_cat = object['category'][i]
            initial[each_cat[0]['name']] = {}
            object['attribute'][i].forEach((ee, ii) => {
                initial[each_cat[0]['name']][ee['name']] = {}
                if (freeLevel === 0){
                    initial[each_cat[0]['name']][ee['name']]['status'] = true
                } else {
                    initial[each_cat[0]['name']][ee['name']]['status'] = false
                }
                initial[each_cat[0]['name']][ee['name']]['free'] = ee['free']
                initial[each_cat[0]['name']][ee['name']]['category'] = each_cat[0]['id']
                initial[each_cat[0]['name']][ee['name']]['attribute'] = ee['id']
            })  
        })
    }

    const initializeColor2= (initial, freeLevel) => {
        let tmp = state.state['cluster']['color']
        tmp['attribute'].forEach((ee, ii) => {
            tmp['attribute'][ii].map((eee, iii)=>{
                let new_catName = tmp['category'][ii][0]['name']
                let new_attrName = tmp['attribute'][ii][iii]['name']
    
                if (initial[new_catName] === undefined){
                    initial[new_catName] = {}
                }
                initial[new_catName][new_attrName] = {}
    
                if (freeLevel === 0){
                    initial[new_catName][new_attrName]['status']  = true
                } else {
                    initial[new_catName][new_attrName]['status'] = false
                }
                initial[new_catName][new_attrName]['free'] = tmp['category'][ii][0]['free']
                initial[new_catName][new_attrName]['category'] = tmp['category'][ii][0]['name']
                initial[new_catName][new_attrName]['attribute'] = tmp['attribute'][ii][iii]['name']
                initial[new_catName][new_attrName]['rgb'] = tmp['attribute'][ii][iii]['rgb']
            })
        })   
    }
    // When you press the Go button, the corresponding items should change to true.
    const handleGoButtonClick = (type) =>{
        let query = ''
        let form = new FormData();

        form.append('ys', window.ys)

        // When you press the Go button, it is sent to the server.
        if (type === 'imageUrl'){
            query = props.styleUrl
            form.append('url', query)
            props.setUrlTC(props.urlTC +1)
        }   
        if (type === 'brandUrl'){
            query = props.brandUrl
            form.append('url', query)
            props.setUrlTC(props.urlTC +1)
        }     
        if (type === 'brandSelect'){
            query = props.brandSelect
            form.append('brand_name', query)
            props.setBrandTC(props.brandTC +1)
        }

        let localhost = origin + 'api'
        let api = '/cat-attr/url'
        let url = localhost + api
        axios.post(url, form
            ).then(async(res)=>{
                var willSelect = res.data
                let copy2 = {...props.category}

                // Color what applies
                Object.keys(copy2).map((k, v)=>{
                    //k shirt, blouse
                    if (willSelect.hasOwnProperty(k)){
                        willSelect[k].map((kk, vv)=>{
                            //kk is washed
                            if (copy2[k].hasOwnProperty(kk)){
                                copy2[k][kk]['status'] = true
                            }
                        })
                    }
                })
        }).catch((err)=>{
        })        
    }

    const handleButtonClick = (e, ee, type) =>{
        if (type == "common_attribute"){
            let arr = {...commonAttr} //When common details change from true to false
            if (arr['common_attribute'][e]['status'] !== undefined){
                arr['common_attribute'][e]['status'] = !arr['common_attribute'][e]['status']
            }
            setCommonAttr(arr)
            //Logic when common detail becomes true
            let copy2 = {...props.category}
            Object.keys(copy2).forEach((element) => {
                if (copy2[element][e] !== undefined){
                    copy2[element][e]['status']  = arr['common_attribute'][e]['status']
                }
            })
            props.setCategory(copy2)
        }

        if (type == "category"){ //One attr must also change from false to false.
            let copy2 = {...props.category}
            if (ee !== null && copy2[e][ee]['status'] !== undefined){
                copy2[e][ee]['status'] = !copy2[e][ee]['status']
            } 
            props.setCategory(copy2)
        }

        if (type == 'color') {
            let copy3 = {...props.color}
            if (ee !== null && copy3[e][ee]['status'] !== undefined){
                copy3[e][ee]['status'] = !copy3[e][ee]['status']
            } 
            props.setColor(copy3)
        }
    }
    return (
        <div className='cat-attr-body'>
            <div className='current-attr-title'>
                <p className='current-attr-label'>Selected attribute : </p><p className='current-attr-number'>{props.finalCount}</p>
            </div>
            <div className='current-attr-title cluster-mix-stack' style={{ display : props.freeLevel === 0 ? 'none' : 'flex'}}>
                <div className='cluster-mix'>Detect image: </div>
                    <div className='cluster-mix-drag'>
                        <input className='cat-attr-input style-image' onChange={(e)=> props.handleInputChange(e, 'imageUrl')} placeholder="Url"></input>
                    </div>
                <div className='btn cluster-mix' onClick={()=> handleGoButtonClick( 'imageUrl') }>Go</div>
            </div>

            <div className='current-attr-title cluster-mix-stack' style={{ display : props.freeLevel === 0 ? 'none' : 'none'}}>
                <div className='cluster-mix'>Upload a brand representative style image: </div>
                    <div className='cluster-mix-drag'>
                        <input className='cat-attr-input brand-image' onChange={(e)=> props.handleInputChange(e, 'brandUrl')} placeholder="url"></input>
                    </div>
                <div className='btn cluster-mix' onClick={()=> handleGoButtonClick('brandUrl') }>Go</div>
            </div>
            <div className='current-attr-title cluster-mix-stack' style={{ display : props.freeLevel === 0 ? 'none' : 'flex'}}>
                <div className='cluster-mix'>Select brand: </div>
                    <div className='cluster-mix-drag'>
                        <select name="fruits" className="cat-attr-select brand-select" onChange={(e)=> props.handleInputChange(e, 'brandSelect')} >
                            <option disabled selected>Brand</option>
                            {
                                props.freeLevel > 0 ? 

                                    Object.values(brands).map((e, i) => {
                                       return <option value={e}>{e}</option> 
                                    })
                                : undefined
                            }
                            
                        </select>
                    </div>
                <div className='btn cluster-mix' onClick={()=> handleGoButtonClick('brandSelect') }>Go</div>
            </div>
            <table className='table table-borderless' style={{ display :'none' }}>
                <thead>
                    <tr>
                        <th>common details</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            {   

                                Object.keys(commonAttr['common_attribute']).map((e, i)=>{
                                    return(
                                        
                                        <button disabled={props.freeLevel === 0 ? true : false} className={btnClassName} onClick={(element)=>{
                                                props.setAttributeTC(props.attributedTC +1)
                                                handleButtonClick(e, null, 'common_attribute')
                                        }} style={{
                                            backgroundColor : (commonAttr['common_attribute'][e]['status']===true && props.finalCount >= 1) ? 'rgb(97 106 120)'  : 'rgb(196, 198, 251)',
                                            color : 'white'
                                        }} >{e}</button>
                                    )
                                })
                            }    
                            {
                                // Number of details selected so far
                                Object.keys(props.category).map((e, i)=>{
                                    Object.keys(props.category[e]).map((ee, ii)=>{
                                        var tmp = props.category[e][ee]['status'] === true && props.freeLevel >= props.category[e][ee]['free'] ?  count += 1 : null;
                                    })
                                })
                            }
                            {
                                //Number of colors selected so far
                                Object.keys(props.color).map((e, i)=>{
                                    Object.keys(props.color[e]).map((ee, ii)=>{
                                        var tmp = props.color[e][ee]['status'] === true && props.freeLevel ?  count += 1 : null;
                                    })
                                })
                            }
                            {   
                                // Number of details selected so far
                                useEffect(()=>{
                                    props.setFinalCount(count)
                                }, [count])
                            }
                        </td>
                    </tr>
                </tbody>
            </table>
            <table className='table table-borderless'>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Detail</th>
                    </tr>
                </thead>
                <tbody>
                    <>
                    {      
                        Object.keys(props.category).map((e, i)=>{
                            //e hue
                            btnClassName = e === 'hue' || e === 'tone' ? 'btn hue-colum' : 'btn btn-attr'
                            return(
                                <tr>
                                    <td style={{display : Object.keys(props.category[e]).some((test) => {
                                       if (  (props.freeLevel === 0 && props.category[e][test]['free'] === 0)
                                        || (props.freeLevel === 1)
                                       ){
                                        return true
                                       }
                                    }) === true ? 'table-cell' : 'none'}}>{e}</td>
                                    { 
                                        <td>
                                        {
                                            Object.keys(props.category[e]).map((ee, ii)=>{
                                                //ee hue0
                                                //ee ['status]

                                                return (                                                    
                                                <button disabled={props.freeLevel === 0 ? true : false} className={btnClassName} 
                                                    onClick={()=>{
                                                        props.setAttributeTC(props.attributedTC +1)
                                                        handleButtonClick(e, ee, 'category')
                                                    }}
                                                    style={{ display : props.category[e][ee]['free'] > props.freeLevel  ? 'none' : 'table-cell', backgroundColor : (props.category[e][ee]['status']===true) ? 'rgb(97 106 120)' : 'rgb(196, 198, 251)'}}>
                                                    {
                                                        e === 'hue' || e === 'tone' ? <HueAttr e={e} category={props.category} shoes={shoes} ee={ee}/> : ee
                                                    }
                                                </button>)
                                            })
                                            
                                        }
                                        </td>
                                    }
                                </tr>
                            ) 
                        })
                    }   
                    {
                        Object.keys(props.color).map((e, i)=>{ 
                            //e vivid
                            btnClassName = e === 'hue' || e === 'tone' ? 'btn hue-colum' : 'btn btn-attr'
                            return(
                                <tr>
                                    <td>{e}</td>
                                    {
                                        <td>
                                        {
                                            Object.keys(props.color[e]).map((ee, ii)=>{
                                                //ee pink
                                                //ee ['status]
                                                return (                                                    
                                                <button disabled={props.freeLevel === 0 ? true : false} className={btnClassName} 
                                                    onClick={()=>{
                                                        props.setAttributeTC(props.attributedTC +1)
                                                        handleButtonClick(e, ee, 'color')
                                                    }}
                                                    style={{ display : props.color[e][ee]['free'] > props.freeLevel  ? 'none' : 'table-cell', backgroundColor : (props.color[e][ee]['status']===true) ? 'rgb(97 106 120)' : 'rgb' + props.color[e][ee]['rgb']}}>
                                                    {ee}
                                                </button>)
                                            })
                                            
                                        }
                                        </td>
                                    }
                                </tr>
                            ) 
                        })
                    } 
                    </>
                </tbody>
            </table>
        </div>
    )
  }

export function HueAttr(props){
    return (
        <LazyLoad>
            <div className='parent-hue'>
                <p className='cat-attr-hue-title'>{props.ee}
                <CustomModal ee={props.ee} e={props.e} category={props.category} /></p>
                    <CustomClusterImages2 ee={props.ee} e={props.e} category={props.category} shoes={props.shoes} params='shoes' class={'cat-attr-hue-image'}/>
            </div>
        </LazyLoad>
    )
} 

import { useLocation, useNavigate, Outlet, json  } from 'react-router-dom'
import React, { useEffect, useState, useCallback, useRef } from "react";
import CustomClusterImages3 from '../CustomClusterImages3.js';
import Button from 'react-bootstrap/Button';
import S3Upload from '../S3Upload.js';
import axios from 'axios';
import CustomSlider from '../CustomSlider.js'
import server from '../servers/data.js'
import local from '../servers/data.js'
 
export default function DesingImprovement(props){
    let origin = ''
    if (window.navigator.userAgent.indexOf('Mac') > 0){
        origin = local['local']
    } else if (window.navigator.userAgent.indexOf('Linux') > 0){
        origin = server['server']    
    }
    const location = useLocation();

    let localhost = origin +'api'
    let stylemixingImages = [];
    const diversity = [1, 2, 3]
    const state = useLocation();
    let [showDiv, setShowDiv] = useState(true)
    const [selectedIGAlgorithm, setSelectedIGAlgorithm] = useState(true)
    // Desing Improvement
    const [isUploaded, setIsUploaded] = useState(0);

    let diversity_ = {1:"Concrete", 2:"Medium", 3:"Abstract"}
    let quality_ = {1:"Low", 2:"Medium", 3:"High"}
    
    const [refresh2, setRefresh2] = useState(0)
    const [refresh3, setRefresh3] = useState(0)
    const [refresh4, setRefresh4] = useState(0)
    const [refresh5, setRefresh5] = useState(0)
    const [refresh6, setRefresh6] = useState(0)
    const [refresh7, setRefresh7] = useState(0)
    const [refresh8, setRefresh8] = useState(0)

    const handleRefresh = (type) => {
      if (type === 'mix1'){
        setRefresh2(prevKey => prevKey +1)
      }
      if (type === 'mix2'){
        setRefresh3(prevKey => prevKey +1)
      }
      if (type === 'mix3'){
        setRefresh4(prevKey => prevKey +1)
      }
      if (type === 'mix4'){
        setRefresh5(prevKey => prevKey +1)
      }
      if (type === 'iter1'){
        setRefresh6(prevKey => prevKey +1)
      }
      if (type === 'inter2'){
        setRefresh7(prevKey => prevKey +1)
      }
      if (type === 'attr1'){
        setRefresh8(prevKey => prevKey +1)
      }      
    };
    
    // Image Generation
    // style-mixing
    const [willgenerateMix, setWillgenerateMix] = useState({'info' : [{'0':[],'1':[],'2':[],'3':[],}], 'method': 'stylemixing', 'degree':1})
    const [isUploadedMix1, setIsUploadedMix1] = useState(0);
    const [inputMix1,setInputMix1] = useState('')
    const [isUploadedMix2, setIsUploadedMix2] = useState(0);
    const [inputMix2,setInputMix2] = useState('')
    const [isUploadedMix3, setIsUploadedMix3] = useState(0);
    const [inputMix3, setInputMix3] = useState('')
    const [isUploadedMix4, setIsUploadedMix4] = useState(0);
    const [inputMix4,setInputMix4] = useState('')
    const [diversityMix, setDiversityMix] = useState(3)
    const [resultMix, setresultMix] = useState('')

    const [selectedFile, setSelectedFile] = useState(null);


    // interpolation
    const [willgenerateInter, setWillgenerateInter] = useState({'info' : [{'0':[],'1':[]}], 'method': 'interpolation'})
    const [isUploadedInter1, setIsUploadedInter1] = useState(0);
    const [isUploadedInter2, setIsUploadedInter2] = useState(0);
    const [inputInter1,setInputInter1] = useState('')
    const [inputInter2,setInputInter2] = useState('')
    const [resultInter, setresultInter] = useState('')

    // attribute-edit
    const [willgenerateAttr, setWillgenerateAttr] = useState({'info' : [{'0':[]}], 'method': 'attributeedit', 'location' : 'upper', 'length' : 'long'})
    const [isUploadedAttr1, setIsUploadedAttr1] = useState(0);
    const [inputAttr1,setInputAttr1] = useState('')
    const [selectedLocationAttr, setSelectedLocationAttr] = useState('')
    const [selectedMethodAttr, setSelectedMethodAttr] = useState('')
    const [resultAttr, setresultAttr] = useState('')

    // backend response
    let [generatedImageArr, setGeneratedImageArr] = useState({})
    let [selectedDiversity, setSelectedDiversity] = useState(1)
    let [selectedQuality, setSelectedQuality] = useState(1)
    let [isChanged, setIsChanged] = useState(false)
    let [backgroundActive, setBackgroundActive] = useState('nav-item-inactive') 
    let [backgroundActive2, setBackgroundActive2] = useState('nav-item-active') 
    let [targetStyle, setTargetStyle] = useState({'' : false, '' : false}) 
    let [selectedStyle, setSelectedStyle] = useState('')
    let [selectedAttr, setSelectedAttr] = useState({})
    let [labelingResult, setLabelingResult] = useState([])

    //log
    let [attributeTC, setAttributeTC] = useState(0)
    let [diversityTC, setDiversityTC] = useState(1)
    let [noiseTC, setNoiseTC] = useState(1)
    let [imageNumTC, setImageNumTC] = useState(0)
    let [changeTC, setChangeTC] = useState(0)
    let [uploadTC, setUploadTC] = useState(0)
    let [recommentTC, setRecommentTC] = useState(0)
    let [styleTC, setStyleTC] = useState(0)

    let [ganGoMixTC, setGanGoMixTC] = useState(0)
    let [ganGoInterTC, setGanGoInterTC] = useState(0)
    let [ganGoAttrTC, setGanGoAttrTC] = useState(0)

    let [ganUploadMixTC, setGanUploadMixTC] = useState(0)
    let [ganUploadInterTC, setGanUploadInterTC] = useState(0)
    let [ganUploadAttrTC, setGanUploadAttrTC] = useState(0)

    // stylemixing, interpolation, attribute-edit
    let [selectedGAN, setSelectedGAN] = useState('stylemixing')
    let [selectedAlgorithm, setSelectedAlgorithm] = useState('')
    let [improveAttr, setImproveAttr] = useState({

        "chic": {
          "improvement": [
            {
              "attribute": "middle skirt",
              "status": false
            },
            {
              "attribute": "upper top",
              "status": false
            }
          ],
          "improvement_images": [
            {
              "url": "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/upload/S_22_bottega-veneta_27.png",
              "score": 9
            }
          ],
          "improvement_score":10, 
          "style": "lovely",
          "score": 15,
          "attention_map": "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/upload/S_22_bottega-veneta_27.png",
          "attention_map_images": [
            {
              "url": "",
              "score": 9
            }
          ]
        },
        "chic2": {
          "improvement": [
            {
              "attribute": "middle skirt",
              "status": false
            },
            {
              "attribute": "upper top",
              "status": false
            }
          ],
          "improvement_images": [
            {
              "url": "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/upload/S_22_bottega-veneta_27.png",
              "score": 9
            }
          ],
          "improvement_score":10, 
          "style": "lovely",
          "score": 15,
          "attention_map": "https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/upload/S_22_bottega-veneta_27.png",
          "attention_map_images": [
            {
              "url": "",
              "score": 9
            }
          ]
        },           
    })       
    // nav-item 
    const navItemHandler = (string) => {
      let url = localhost + '/ds/type/'
      let form = new FormData();
      let array ={
          'toggle' : {
            'page' : ''
          }
      }
      if (string === 'design-imporvement'){
          setBackgroundActive('nav-item-active')
          setBackgroundActive2('nav-item-inactive')
          props.setPhased('design-imporvement')
          array['toggle']['page'] = 'design-improvement'
      }
      if (string === 'image-generation'){
          setBackgroundActive('nav-item-inactive')
          setBackgroundActive2('nav-item-active')
          props.setPhased('image-generation')
          array['toggle']['page'] = 'image-generation'
      }
      array['season'] = window.season

      form.append('log', JSON.stringify(array))
      axios.post(url , form
        ).then(async(res)=>{
        }).catch((err)=>{
      }) 
    } 

    const handleSliderChange = (e, newValue) => {
      setDiversityMix(newValue)
      setImageNumTC(imageNumTC + 1)
    };

    useEffect( () => {
        let initial = {} 
        let initial2 = {...initializeState(initial)}
        setTargetStyle(initial2)
        props.setFreeLevel(1)


        // setSelectedStyle(Object.keys(initial2)[0])

        // for (const i in Object.keys(initial2)){
        //   let tmp = {...selectedAttr}
        //   tmp[selectedStyle] = {}
        //   setSelectedAttr(tmp)
        // }

    }, []);

    useEffect(()=>{
      
  }, [isUploadedMix1])

    // If the AI degree of freedom is text, it is always in text format.
    useEffect( () => {
      // setSelectedAlgorithm('text')
  }, [props.freeLevel]);

  // When the algorithm changes, the selected style is reset
    useEffect( () => {
      // setSelectedStyle('')
      setIsChanged(true)
  }, [selectedAlgorithm]);

  // Communication must be made every time the image changes.
    useEffect(() => {
      async function fetchData (){
        let initial2 = {}
        let initial3 = await initializeImproveAttr(initial2)
        setImproveAttr(initial3)
      };
      fetchData()
  }, [isUploaded]);

  useEffect(() => {
    setShowDiv(true)
  }, [improveAttr]);

    // ImproveAttr changes when the image changes. Redraw the screen every time
    const initializeImproveAttr = (initial2) => {
      let tmp = state.state
      return tmp
    }
    // Initialize to the state received from communication
    const initializeState = (initial) => {

        // let tmp = {'target_design': ['chic3', 'chic4']}
        let tmp = state.state['cluster']['target_design']
        // tmp.map((v, i) => {
        tmp.map((v, i) => {
            initial[v] = false
        })
        return initial
      // })
    }

    const handleChange = (event, type) => {
      if (type === 'mix1'){
        setInputMix1(event.target.value);
      } else if (type === 'mix2'){
        setInputMix2(event.target.value);
      }else if (type === 'mix3'){
        setInputMix3(event.target.value);
      }else if (type === 'mix4'){
        setInputMix4(event.target.value);
      }else if (type === 'inter1'){
        setInputInter1(event.target.value);
      }else if (type === 'inter2'){
        setInputInter2(event.target.value);
      } else if (type === 'attr1'){
        setInputAttr1(event.target.value);
      }           
    };

    const handleGoBtn = (e, type) => {

      handleRefresh(type)
      //1,1,'dark_punk', 1
      let url = ''
      let dict = {}
      
      if (type === 'mix1'){
        
        let tmp = inputMix1.split(',')
        generatedImageArr['info'].map((v, i) => {
          if (v['diversity'] === tmp[0] && v['quality'] === tmp[1] && v['style'] === tmp[2].replace('\'', '').replace('\"', '') && v['number'] === parseInt(tmp[3])){ 
            url = v['url']
            dict= v
          }
        })
        setIsUploadedMix1(url)
        willgenerateMix['info']['0'] = dict
        setGanGoMixTC(ganGoMixTC+1)
      }else if (type === 'mix2'){
        let tmp = inputMix2.split(',')
        generatedImageArr['info'].map((v, i) => {
          if (v['diversity'] ===tmp[0] && v['quality'] === tmp[1] && v['style'] === tmp[2].replace('\'', '').replace('\"', '') && v['number'] === parseInt(tmp[3])){
            url = v['url']
            dict = v
          }
        })
        setIsUploadedMix2(url)
        willgenerateMix['info']['1'] = dict
        setGanGoMixTC(ganGoMixTC+1)
      } else if (type === 'mix3'){
        let tmp = inputMix3.split(',')
        generatedImageArr['info'].map((v, i) => {
          if (v['diversity'] === tmp[0] && v['quality'] === tmp[1] && v['style'] === tmp[2].replace('\'', '').replace('\"', '') && v['number'] === parseInt(tmp[3])){
            url = v['url']
            dict = v
          }
        })
        setIsUploadedMix3(url)
        willgenerateMix['info']['2'] = dict
      }else if (type === 'mix4'){
        let tmp = inputMix4.split(',')
        generatedImageArr['info'].map((v, i) => {
          if (v['diversity'] === tmp[0] && v['quality'] === tmp[1] && v['style'] === tmp[2].replace('\'', '').replace('\"', '') && v['number'] === parseInt(tmp[3])){
            url = v['url']
            dict = v
          }
        })
        setIsUploadedMix4(url)
        willgenerateMix['info']['3'] = dict
        
      } else if (type === 'inter1'){
        let tmp = inputInter1.split(',')
        generatedImageArr['info'].map((v, i) => {
          if (v['diversity'] === tmp[0] && v['quality'] === tmp[1] && v['style'] === tmp[2].replace('\'', '').replace('\"', '') && v['number'] === parseInt(tmp[3])){
            url = v['url']
            dict = v
          }
        })
        setIsUploadedInter1(url)
        willgenerateInter['info']['0'] = dict
        setGanGoInterTC(ganGoInterTC+1)
      } else if (type === 'inter2'){
        let tmp = inputInter2.split(',')
        generatedImageArr['info'].map((v, i) => {
          if (v['diversity'] === tmp[0] && v['quality'] === tmp[1] && v['style'] === tmp[2].replace('\'', '').replace('\"', '') && v['number'] === parseInt(tmp[3])){
            url = v['url']
            dict = v
          }
        })
        setIsUploadedInter2(url)
        willgenerateInter['info']['1'] = dict
        setGanGoInterTC(ganGoInterTC+1)
      } else if (type === 'attr1'){
        let tmp = inputAttr1.split(',')
        generatedImageArr['info'].map((v, i) => {
          if (v['diversity'] === tmp[0] && v['quality'] ===tmp[1] && v['style'] === tmp[2].replace('\'', '').replace('\"', '') && v['number'] === parseInt(tmp[3])){
            url = v['url']
            dict = v
          }
        })
        setIsUploadedAttr1(url)
        willgenerateAttr['info']['0'] = dict
        setGanGoAttrTC(ganGoAttrTC+ 1)
      } 
    }

    return (
        <>
            <div className='ds-container' >
                <div className='ds-body'>
                    <div className='ds-select-left'>
                        <div className='ds-left' >  
                            <div className='ds-flex-item'>
                                <div className='nav-title purple' >
                                    CoCoStyle
                                </div>
                                <div className={`ds-nav-item ${backgroundActive2}`}  onClick={()=>navItemHandler('image-generation')}>
                                    CoDesign
                                </div>
                                <div className={`ds-nav-item ${backgroundActive}`} onClick={()=>navItemHandler('design-imporvement')}>
                                    CoImprove
                                </div>

                            </div>
                        </div>
                    </div>
                    <div className='ds-right' style={{display : props.phase === 'design-imporvement' ? 'block' : 'none'}}>
                        <div className='ds-right-algorithm' > 
                          <div className='ds-right-algorithm-child'>Choose method</div>
                          <div className={`${selectedAlgorithm === 'text' ? 'btn btn-dark': 'btn'} ds-right-algorithm-child`}
                            onClick={(e)=>{
                              setSelectedAlgorithm('text')

                              let url = localhost + '/ds/improvement/style'
                              let form = new FormData();

                              let array ={
                                  'clicked' : {
                                    'method' : 'styleVIEW',
                                    'upload' : uploadTC,
                                    'attribute' :  attributeTC
                                  },
                              }
                              array['season'] = window.season

                              form.append('log', JSON.stringify(array))

                              axios.post(url , form
                                ).then(async(res)=>{

                                  let tmp2 = {...improveAttr}
                                  tmp2[selectedStyle]['improvement_images'] = res.data['improvement_images']
                                  setImproveAttr(tmp2)
                                }).catch((err)=>{

                              }) 

                            }}>Style FIT</div>
                          <div className={`${selectedAlgorithm === 'image' ? 'btn btn-dark': 'btn'} ds-right-algorithm-child`}
                          style={{display : props.freeLevel > 0? 'block' : 'none'}}
                            onClick={(e)=>{
                              setSelectedAlgorithm('image')
                              let url = localhost + '/ds/improvement/style'
                              let form = new FormData();

                              let array ={
                                  'clicked' : {
                                    'method' : 'styleFIT',
                                    'upload' : uploadTC,
                                    'attribute' : recommentTC
                                  },
                              }
                              array['season'] = window.season

                              form.append('log', JSON.stringify(array))

                              axios.post(url , form
                                ).then(async(res)=>{

                                  let tmp2 = {...improveAttr}
                                  tmp2[selectedStyle]['improvement_images'] = res.data['improvement_images']
                                  setImproveAttr(tmp2)
                                }).catch((err)=>{
                              }) 
                            }}>Style VIEW</div> 
                        </div> 

                        <div style={{display : selectedAlgorithm !== '' ? 'block' : 'none'}}> 
                          <div className='ds-right-explain'> 
                            <div style={{ display : props.phase === 'design-imporvement' && selectedAlgorithm !== '' ? 'none' : 'none'}}>
                              </div> 
                          </div>
                          <div className='target-style' style={{ display : selectedAlgorithm === 'text' ? 'flex' : 'none'}}>
                            <div className='ds-right-explain-target-style' > Style</div>
                            {
                                Object.keys(targetStyle).map((v, i) =>{
                                    return <button 
                                        className={ `${targetStyle[v] === false  ? 'btn': 'btn btn-dark'} btn target-style-btn`} 
                                        onClick={(e)=>{
                                            let tmp = {...targetStyle}
                                            Object.keys(targetStyle).map((vv, ii) =>{
                                                tmp[[vv]] = false
                                            })

                                            tmp[v] = !tmp[v]
                                            setIsChanged(false)
                                            setTargetStyle(tmp)
                                            setSelectedStyle(v)
                                            setRecommentTC(recommentTC+1) 
                                    }}>{v}</button>
                                })
                            }
                          </div>
                          <div className='my-style-container'>
                                <div className='my-style-left'>
                                    <div className='my-style-text'>Image</div>
                                    <S3Upload type2='improve' setUploadTC={setUploadTC} uploadTC={uploadTC} type='user-target' selectedAlgorithm={selectedAlgorithm} setLabelingResult={setLabelingResult} setSelectedFile={setSelectedFile} setIsUploaded={setIsUploaded} selectedStyle={selectedStyle} isUploaded={isUploaded} improveAttr={improveAttr} setSelectedStyle={setSelectedStyle} setImproveAttr={setImproveAttr}/>
                                </div>
     
                                <div style={{ display : selectedAlgorithm === 'text' && selectedStyle !=='' &&  improveAttr &&improveAttr[selectedStyle] && improveAttr[selectedStyle]['improvement']? 'block' : 'none'}} className='my-style-right'>
                                    <div className='my-style-right-text'>Attribute</div>
                                    <div className='my-style-right-scroll'>
                                    {
                                      isUploaded > 0 && showDiv && selectedStyle !==''&&  improveAttr &&improveAttr[selectedStyle] && improveAttr[selectedStyle]['improvement'] ?  <div className='my-style-fix-attr-container'  style={{ display : selectedStyle === ''  ? 'none' : 'block'}}>         
                                      {
                                          improveAttr[selectedStyle]['improvement'].map((v, i) => {
                                              return <button className={`${  selectedAttr.hasOwnProperty(selectedStyle) && selectedAttr[selectedStyle].includes(v['attribute']) ? 'btn-dark': 'btn'} 'btn my-style-fix-attr`}
                                                  onClick={async (e)=>{
                                                      //api/ds/improvement/attribute
                                                      let url = localhost + '/ds/improvement/attribute'
                                                      let form = new FormData();
                                                      
                                                      let tmp = {}
                                                      if (selectedAttr.hasOwnProperty(selectedStyle) && selectedAttr[selectedStyle].length > 0 ){
                                                        tmp[selectedStyle] = [...selectedAttr[selectedStyle]]
                                                        if ( tmp[selectedStyle].includes(v['attribute'])){
                                                          tmp[selectedStyle] = tmp[selectedStyle].filter(item => item !== v['attribute'])
                                                        } else {
                                                          tmp[selectedStyle].push(v['attribute'])
                                                        }
                                                      }else {
                                                        tmp[selectedStyle] = []
                                                        tmp[selectedStyle].push(v['attribute'])
                                                      }
                                                        
                                                      setSelectedAttr(tmp)
                                                      form.append('attribute', JSON.stringify(tmp[selectedStyle]))
                                                      form.append('image', JSON.stringify(selectedFile))
                                                      form.append('style', JSON.stringify(selectedStyle))
                                                      form.append('labeling_result', JSON.stringify(labelingResult['labeling_result'])) 
                                                      
                                                      await axios.post(url , form
                                                        ).then(async(res)=>{

                                                          let tmp2 = {...improveAttr}
                                                          tmp2[selectedStyle]['improvement_images'] = res.data['improvement_images']
                                                          setImproveAttr(tmp2)
                                                          setRecommentTC(recommentTC+1)
                                                        }).catch((err)=>{

                                                      }) 
                                                  }} 
                                              >{v['attribute']}</button>
                                          }) 
                                      }
                                      
                                  </div>:  <div className='my-style-fix-attr-container'>
                                        <button className='btn my-style-fix-attr'></button>
                                        <button className='btn my-style-fix-attr'></button>
                                        <button className='btn my-style-fix-attr'></button>
                                        <button className='btn my-style-fix-attr'></button>
                                        <button className='btn my-style-fix-attr'></button>
                                        <button className='btn my-style-fix-attr'></button>
                                        <button className='btn my-style-fix-attr'></button>
                                        <button className='btn my-style-fix-attr'></button>
                                    </div>
                                  } 
                                  </div>
                                </div>
                              <div style={{ display : selectedAlgorithm === 'image' && isUploaded > 0 && showDiv  && props.freeLevel > 0 && isUploaded > 0  && selectedStyle !=='' &&  improveAttr &&improveAttr[selectedStyle] && improveAttr[selectedStyle]['attention_map'] ? 'none' : 'none'}} className='my-style-right'>
                                  <div style={{ display : selectedAlgorithm === 'image' && isUploaded > 0 && showDiv ? 'flex' : 'none'}} className='my-style-attention-map'> { isUploaded > 0 && showDiv && selectedStyle !=='' &&  improveAttr &&improveAttr[selectedStyle] && improveAttr[selectedStyle]['style']? <>{improveAttr[selectedStyle]['style']}, {improveAttr[selectedStyle]['score']}</> : <></> }</div>
                                  <div className='my-style-parent-container' style={{ display : isUploaded > 0  && selectedStyle !=='' &&  improveAttr &&improveAttr[selectedStyle] && improveAttr[selectedStyle]['attention_map'] ? 'flex' : 'none'}}>
                                      <img className='my-style-file-img' style={{ visibility : isUploaded > 0 ? 'visible' : 'hidden'}} src={isUploaded > 0  && selectedStyle !=='' &&  improveAttr &&improveAttr[selectedStyle] && improveAttr[selectedStyle]['attention_map']? improveAttr[selectedStyle]['attention_map'] :  <></>}/>
                                  </div>
                              </div>
                          </div>
                          <div className=' target-style' style={{ display : selectedAlgorithm === 'image' && isUploaded > 0 && showDiv ? 'flex' : 'none'}}>
                              <div className='another-style ds-right-explain-target-style'>Style</div>
                              {
                                  Object.keys(targetStyle).map((v, i) =>{
                                      return <button 
                                          className={ `${targetStyle[v] === false   ? 'btn': 'btn btn-dark'} btn another-style target-style-btn`} 
                                          onClick={(e)=>{
                                              let tmp = {...targetStyle}
                                              
                                              Object.keys(targetStyle).map((vv, ii) =>{
                                                  tmp[[vv]] = false
                                              })

                                              tmp[v] = !tmp[v]
                                              setIsChanged(false)
                                              setTargetStyle(tmp)
                                              setSelectedStyle(v)
                                              setAttributeTC(attributeTC +1)
                                      }}>{v}</button>
                                  })
                              }
                            </div>
                        <div className='my-style-score' style={{ display : selectedStyle === '' ? 'none' : 'block'}}> 
                          <div style={{ display : selectedAlgorithm === 'image' ? 'none' : 'none'}}>
                            { isUploaded > 0 && showDiv && selectedStyle !=='' && selectedAlgorithm === 'text' &&  improveAttr &&improveAttr[selectedStyle] && improveAttr[selectedStyle]['improvement_score']? improveAttr[selectedStyle]['improvement_score'] : <></>} 
                          </div>
                        </div>                      
                          <div className='improvement-container-text' style={{ display : (selectedStyle !== '' ) ? 'flex' : 'none'}}> { selectedAlgorithm === 'text' ? "" : "" }</div>
                          <div className='improvement-container' style={{ display : selectedStyle !== ''  ? 'flex' : 'none'}}> 
                            <div className='improvement-container-sub'>
                              {
                                isUploaded > 0 &&  selectedStyle !=='' &&  improveAttr && improveAttr[selectedStyle] ? 
                                  selectedAlgorithm === 'image' && selectedStyle !== '' 
                                  ? improveAttr[selectedStyle]['attention_map_images'].map((v, i) => {
                                    return ( 
                                        <div className='improvement-example-sub' >
                                          <img className='improvement-example-image-real' src={v['url']}/>
                                          <div className='improvement-example-score' style={{ display : 'none'}}> {v['score']}</div>
                                        </div>
                                    )                                    
                                }) : 
                                  improveAttr[selectedStyle]['improvement_images'].map((v, i) => {
                                      return ( 
                                          <div className='improvement-example-sub' >
                                            <img className='improvement-example-image-real' src={v['url']}/>
                                            <div className='improvement-example-score' style={{ display : 'none'}}>{v['score']}</div>
                                          </div>
                                      )                                    
                                  }) 
                                  :
                                  <>{}</>
                              }
                              </div>
                          </div>
                          <div className='improvement-container' style={{ display :  selectedStyle !== '' ? 'none' : 'flex'}}> 
                              <div className='improvement-example-image'></div>
                              <div className='improvement-example-image'></div>
                              <div className='improvement-example-image'></div>
                              <div className='improvement-example-image'></div> 
                              <div className='improvement-example-image'></div>
                              <div className='improvement-example-image'></div>
                          </div>
                          <div className='improvement-container' style={{ display : (selectedStyle !== '') ? 'none' : 'flex'}}> 
                              <div className='improvement-example-score2' ></div>
                              <div className='improvement-example-score2' ></div>
                              <div className='improvement-example-score2' ></div>
                              <div className='improvement-example-score2' ></div>
                              <div className='improvement-example-score2' ></div>
                              <div className='improvement-example-score2' ></div>
                          </div>

                      </div>
                    </div>
                    <div className='ds-right' style={{display : props.phase === 'image-generation' ? 'block' : 'none'}}>
                    <div style={{ display : props.phase !== 'design-imporvement' ? 'none' : 'none'}}>
              
                    </div> 

                        <div className='target-style' style={{display : props.freeLevel === 0 ? 'flex' : 'none'}}>
                          <div></div>
                          <button className='btn btn-dark target-style-btn' ></button>
                        </div> 
                        <div className='target-style' style={{display : props.freeLevel === 1 ? 'flex' : 'none'}}>
                            <div className='text-width'>Diversity level</div>
                            {
                              diversity.map((v, i) => {
                                return <button 
                                        className={ `${ selectedDiversity === v ? 'btn btn-dark': 'btn '} btn target-style-btn`} 
                                        onClick={(e)=>{
                                          setSelectedDiversity(v)
                                          setDiversityTC(diversityTC +1)
                                    }}>{diversity_[v]}</button>
                              })
                            }
                        </div>
                        <div className='target-style' style={{display : props.freeLevel === 1 ? 'flex' : 'none'}}>
                          <div className='text-width'>Quality level</div>
                          {
                              diversity.map((v, i) => {
                                return <button 
                                        className={ `${ selectedQuality === v ? 'btn btn-dark': 'btn '} btn target-style-btn`} 
                                        onClick={(e)=>{
                                          setSelectedQuality(v)
                                          setNoiseTC(noiseTC +1)
                                    }}>{quality_[v]}</button>
                              })
                            }                          
                        </div>
                        <div className='target-style'>
                          <div className='text-width'>Style</div>
                          {
                                Object.keys(targetStyle).map((v, i) =>{
                                    return <button 
                                        className={ `${targetStyle[v] === false || isChanged === true ? 'btn': 'btn btn-dark'} btn target-style-btn`} 
                                        onClick={(e)=>{
                                            let tmp = {...targetStyle}
                                            Object.keys(targetStyle).map((vv, ii) =>{
                                                tmp[[vv]] = false
                                            })

                                            tmp[v] = !tmp[v]
                                            setIsChanged(false)
                                            setTargetStyle(tmp)
                                            setSelectedStyle(v)
                                            setStyleTC(styleTC + 1)
                                    }}>{v}</button>
                                })
                            }
                        </div>
                        <div>
                          <button className='btn generate-btn'
                            onClick={(e)=>{
                              //api/ds/ImageGeneration/generate
                              let url = localhost + '/ds/ImageGeneration/generate'
                              let array = {
                                'clicked' :{ 
                                  'method' : 'generation1',
                                  'diversity' : diversityTC,
                                  'noise' : noiseTC,
                                  'style' : styleTC
                                },
                              }
                              array['season'] = window.season
                              let form = new FormData();
                              form.append('diversity', JSON.stringify(selectedDiversity))
                              form.append('quality',JSON.stringify(selectedQuality))
                              form.append('style', JSON.stringify(selectedStyle))
                              form.append('log', JSON.stringify(array))

                              axios.post(url , form
                                ).then(async(res)=>{
                                  //FIX ME : 
                                  let tmp = {...res.data}
                                  setGeneratedImageArr(tmp)
                                }).catch((err)=>{
                              }) 
                            }}
                          disabled={ selectedStyle === '' ? true : false }
                          >Generate</button>
                        </div>
                        <div className='box-wrapper'>
                          <div className='naming-images-box'>
                            <CustomClusterImages3 info={generatedImageArr} freeLevel={props.freeLevel}/>
                          </div>
                        </div>
                      <div className='gan-parent-container' style={{ display : props.freeLevel > 0 && Object.keys(generatedImageArr).length > 0 ? 'block' : 'none'}}>
                        <div style={{ display : props.freeLevel > 0  ? 'flex' : 'none'}}>
                          <div className='gan-type-box' > 
                            <div className='ds-right-algorithm-child'>Choose function</div>
                            <div className={`${selectedGAN === 'stylemixing' ? 'btn btn-dark': 'btn'} ds-right-algorithm-child`}
                              onClick={(e)=>{
                                setSelectedGAN('stylemixing')
                              }}>Style mixing
                            </div>
                            <div className={`${selectedGAN === 'interpolation' ? 'btn btn-dark': 'btn'} ds-right-algorithm-child`}
                              onClick={(e)=>{
                                setSelectedGAN('interpolation')
                              }}>Interpolation
                            </div> 
                            <div className={`${ selectedGAN=== 'attributeedit' ? 'btn btn-dark': 'btn'} ds-right-algorithm-child`}
                              onClick={(e)=>{
                                setSelectedGAN('attributeedit')
                              }}>Attribute edit
                            </div>
                          </div>
                        </div>
                        <div className='change-degree' style={{ display : props.freeLevel > 0 && selectedGAN === 'stylemixing'? 'flex' : 'none'}}>
                          <div className='change-text'>Choose how to mix image</div>
                          <div className='change-slide'>
                            <div>Image1</div>
                            <CustomSlider
                                aria-label="Volume"
                                defaultValue={3} 
                                step={1}
                                min={1}
                                max={5}
                                onChange={handleSliderChange}
                                value={diversityMix}
                            />
                            <div>Image2</div>
                          </div>
                        </div>
                        <div className='change-degree' style={{ display : props.freeLevel > 0  && selectedGAN === 'attributeedit' ? 'flex' : 'none'}}> 
                            <div className='ds-right-algorithm-child'>Choose part</div>
                            <div className={`${ selectedLocationAttr === 'upper' ? 'btn btn-dark': 'btn'} attribute-edit-change`}
                              onClick={(e)=>{
                                setSelectedLocationAttr('upper')
                                setChangeTC(changeTC + 1)
                              }}> Upper
                            </div>
                            <div className={`${selectedLocationAttr === 'bottom' ? 'btn btn-dark': 'btn'} attribute-edit-change`}
                              onClick={(e)=>{
                                setSelectedLocationAttr('bottom')
                                setChangeTC(changeTC + 1)
                              }}> Bottom
                            </div> 
                        </div>
                        <div className='change-degree' style={{ display : props.freeLevel > 0  && selectedGAN === 'attributeedit' ? 'flex' : 'none'}}> 
                            <div className='ds-right-algorithm-child'>Choose length</div>
                            <div className={`${ selectedMethodAttr === 'long' ? 'btn btn-dark': 'btn'} attribute-edit-change`}
                              onClick={(e)=>{
                                setSelectedMethodAttr('long')
                              }}> Long
                            </div>
                            <div className={`${selectedMethodAttr === 'short' ? 'btn btn-dark': 'btn'} attribute-edit-change`}
                              onClick={(e)=>{
                                setSelectedMethodAttr('short')
                              }}> Short
                            </div> 
                        </div>
                        <div>  
                          <button className='btn generate-btn'
                          style={{ display : props.freeLevel > 0  ? 'flex' : 'none'}}
                            onClick={async (e)=>{
                              stylemixingImages.push(isUploadedMix1)
                              stylemixingImages.push(isUploadedMix2)
                              stylemixingImages.push(isUploadedMix3)
                              stylemixingImages.push(isUploadedMix4)

                              // FIX ME : 
                              let localhost = origin +'api'
                              let url = localhost + '/ds/ImageGeneration/imagegeneration'
                              let form = new FormData();

                              if (selectedGAN === 'stylemixing'){
                                  let array = {
                                    'clicked' : {
                                      'method' : 'stylemixing',
                                      'upload' : ganUploadMixTC,
                                      'go' : ganGoMixTC,
                                      'image_num' : imageNumTC
                                    },
                                  }
                                  array['season'] = window.season
                                  willgenerateAttr['method'] = 'stylemixing'
                                  willgenerateMix['degree'] = diversityMix
                                  setWillgenerateMix({...willgenerateMix})

                                  form.append('method', 'stylemixing')
                                  form.append('degree', JSON.stringify(diversityMix))
                                  form.append('info', JSON.stringify(willgenerateMix['info']))
                                  form.append('log', JSON.stringify(array))

                                  await axios.post(url , form
                                    ).then(async(res)=>{
                                        setresultMix('')
                                        setresultMix(res.data['url'])
                                    }).catch((err)=>{
                                    })
    
                              } else if (selectedGAN === 'interpolation'){
                                let array = {
                                  'clicked' : {
                                    'method' : 'interpolation',
                                    'upload' : ganUploadInterTC,
                                    'go' : ganGoInterTC,
                                  },
                                }
                                array['season'] = window.season
                                willgenerateInter['method'] = 'interpolation'
                                setWillgenerateInter({...willgenerateInter})
                                form.append('method', 'interpolation')
                                form.append('info', JSON.stringify(willgenerateInter['info']))
                                form.append('log', JSON.stringify(array))
                                await axios.post(url , form
                                  ).then(async(res)=>{
                                      setresultInter('')
                                      setresultInter(res.data['url'])
                                  }).catch((err)=>{
                                  })

                                 
                              } else if (selectedGAN === 'attributeedit'){
                                let array = {
                                  'clicked' : {
                                    'method' : 'attributeedit',
                                    'upload' : ganUploadAttrTC,
                                    'go' : ganGoAttrTC,
                                    'change' :changeTC  
                                  },
                                }
                                array['season'] = window.season
                                willgenerateAttr['location'] = selectedLocationAttr
                                willgenerateAttr['length'] = selectedMethodAttr
                                willgenerateAttr['method'] = 'attributeedit'
                                setWillgenerateAttr({...willgenerateAttr})
                                
                                form.append('method', 'attributeedit')
                                form.append('length', JSON.stringify(selectedMethodAttr))
                                form.append('location', JSON.stringify(selectedLocationAttr))
                                form.append('info', JSON.stringify(willgenerateAttr['info']))
                                form.append('log', JSON.stringify(array))
                                
                                await axios.post(url , form
                                  ).then(async(res)=>{
                                      setresultAttr('')
                                      setresultAttr(res.data['url'])
                                  }).catch((err)=>{
                                  })
                              }
                            }}
                          >Generate</button>
                        </div>
                        <div className='interpolation-img-container' style={{ display : props.freeLevel > 0 && selectedGAN === 'stylemixing' ? 'flex' : 'none'}}>
                          <div key={refresh2} className='interpolation-img-container-sub'>
                          {<S3Upload className='stylemixing-img' setGanUploadMixTC={setGanUploadMixTC} ganUploadMixTC={ganUploadMixTC} mixtype={1} array={willgenerateMix} type='style-mixing' setSelectedFile={setSelectedFile} setIsUploaded={setIsUploadedMix1} isUploaded={isUploadedMix1}/>}
                            <div className='stylemixing-input'>
                              <input className='user-input-gan' onChange={(e) => {handleChange(e, 'mix1')}} placeholder='Diversity, Quality, Style, Image'></input>
                              <div className='btn gan-go' onClick={(e)=> {handleGoBtn(e, 'mix1')} }>Go</div>  
                            </div>
                          </div>
                          <div className='interpolation-img-container-sub'>
                            <S3Upload key={refresh3} className='stylemixing-img' setGanUploadMixTC={setGanUploadMixTC} ganUploadMixTC={ganUploadMixTC} mixtype={2} array={willgenerateMix} type='style-mixing' setSelectedFile={setSelectedFile} setIsUploaded={setIsUploadedMix2} isUploaded={isUploadedMix2}/>
                            <div className='stylemixing-input'>
                              <input className='user-input-gan' onChange={(e) => {handleChange(e, 'mix2')}}   placeholder='Diversity, Quality, Style, Image'></input>
                              <div className='btn gan-go' onClick={(e)=> {handleGoBtn(e, 'mix2')} }>Go</div>    
                            </div>
                          </div>
                          {/* <div className='stylemixing-img-container-sub'> */}
                            {/* <S3Upload key={refresh4} className='stylemixing-img' mixtype={3} array={willgenerateMix}  type='style-mixing' setSelectedFile={setSelectedFile} setIsUploaded={setIsUploadedMix3} isUploaded={isUploadedMix3}/> */}
                            {/* <div className='stylemixing-input'> */}
                              {/* <input className='user-input-gan' onChange={(e) => {handleChange(e, 'mix3')}}  placeholder='Diversity, Quality, Style, Image'></input> */}
                              {/* <div className='btn gan-go' onClick={(e)=> {handleGoBtn(e, 'mix3')} }>Go</div>   */}
                            {/* </div> */}
                          {/* </div> */}
                          {/* <div className='stylemixing-img-container-sub'> */}
                            {/* <S3Upload key={refresh5} className='stylemixing-img' mixtype={4} array={willgenerateMix} type='style-mixing' setSelectedFile={setSelectedFile} setIsUploaded={setIsUploadedMix4} isUploaded={isUploadedMix4}/> */}
                            {/* <div className='stylemixing-input'>
                              <input className='user-input-gan' onChange={(e) => {handleChange(e, 'mix4')}}  placeholder='Diversity, Quality, Style, Image'></input>
                              <div className='btn gan-go' onClick={(e)=> {handleGoBtn(e, 'mix4')} }>Go</div>  
                            </div> */}
                          {/* </div> */}
                          <div style={{ display : props.freeLevel > 0 && selectedGAN === 'stylemixing' ? 'flex' : 'none'}}>
                            <div className='my-gan-parent-container'>
                              <div style={{ display : resultMix === '' ? 'flex' : 'none'}} className='gan-result-container'></div>
                              <img style={{ display : resultMix !== '' ? 'flex' : 'none'}}  className='my-style-file-img'  src={resultMix}/>
                            </div>
                          </div>
                        </div>

                       

                        {/* // interpolation  */}
                        <div className='interpolation-img-container' style={{ display : props.freeLevel > 0 && selectedGAN === 'interpolation' ? 'flex' : 'none'}}>
                          
                        <div className='interpolation-img-container-sub'>
                            <S3Upload key={refresh6} ganUploadInterTC={ganUploadInterTC} setGanUploadInterTC={setGanUploadInterTC} className='interpolation-img' intertype={1}  array={willgenerateInter} type='interpolation' setSelectedFile={setSelectedFile} setIsUploaded={setIsUploadedInter1} isUploaded={isUploadedInter1}/>
                              <div className='stylemixing-input'>
                                <input className='user-input-gan' onChange={(e) => {handleChange(e, 'inter1')}}   placeholder='Diversity, Quality, Style, Image'></input>
                                <div className='btn gan-go' onClick={(e)=> {handleGoBtn(e, 'inter1')} }>Go</div>  
                              </div>
                            </div>

                          <div className='interpolation-img-container-sub'  >
                            <div className='my-gan-parent-container'>
                              <div className='gan-result-container' style={{ display : props.freeLevel > 0 && selectedGAN === 'interpolation' && resultInter === '' ? 'flex' : 'none'}}></div>
                              <img className='my-style-file-img' style={{ display : props.freeLevel > 0 && selectedGAN === 'interpolation' &&resultInter !== '' ? 'flex' : 'none'}} src={resultInter}/>
                            </div>
                          </div>

                          <div className='interpolation-img-container-sub'>
                            <S3Upload key={refresh7} ganUploadInterTC={ganUploadInterTC} setGanUploadInterTC={setGanUploadInterTC} className='interpolation-img' intertype={2} array={willgenerateInter} type='interpolation' setSelectedFile={setSelectedFile} setIsUploaded={setIsUploadedInter2} isUploaded={isUploadedInter2}/>
                              <div className='stylemixing-input'>
                                <input className='user-input-gan' onChange={(e) => {handleChange(e, 'inter2')}}   placeholder='Diversity, Quality, Style, Image'></input>
                                <div className='btn gan-go' onClick={(e)=> {handleGoBtn(e, 'inter2')} }>Go</div>  
                              </div>
                            </div>
                        </div>

                        {/* //attributeedit   */}
                        <div className='attributeedit-img-container' style={{ display : props.freeLevel > 0 && selectedGAN === 'attributeedit' ? 'flex' : 'none'}}>
                          <div className='attributeedit-img-container-sub'>
                            <S3Upload key={refresh8} ganUploadAttrTC={ganUploadAttrTC} setGanUploadAttrTC={setGanUploadAttrTC} className='stylemixing-img' attrtype={1} array={willgenerateAttr} type='attributeedit' setSelectedFile={setSelectedFile} setIsUploaded={setIsUploadedAttr1} isUploaded={isUploadedAttr1}/>
                            <div className='stylemixing-input'>
                            <input className='user-input-gan' onChange={(e) => {handleChange(e, 'attr1')}}   placeholder='Diversity, Quality, Style, Image'></input>
                                <div className='btn gan-go' onClick={(e)=> {handleGoBtn(e, 'attr1')} }>Go</div>  
                            </div>
                          </div>
                          <div className='attributeedit-img-container-sub'>
                            <div className='my-gan-parent-container'>
                              <div className='gan-result-container attributeedit' style={{ display : props.freeLevel > 0 && selectedGAN === 'attributeedit' && resultAttr === '' ? 'flex' : 'none'}}></div>
                              <img className='my-style-file-img attributeedit' style={{ display : props.freeLevel > 0 && selectedGAN === 'attributeedit' &&resultAttr !== '' ? 'flex' : 'none'}} src={resultAttr}/>
                            </div>
                          </div>                       
                        </div>
                    </div>
                    </div>
                </div>
            </div>    
        </>
    )
  }
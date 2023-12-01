import './App.css';
import axios from 'axios'
import React, { useEffect, useState, useCallback } from "react";
import {  Route, HashRouter as Router, Routes, Link } from 'react-router-dom';
import {  useNavigate, Outlet, useLocation } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import MenuStart from './routes/Start.js'
import CatAttr from './routes/CatAttr.js'
import Cluster from './routes/Cluster.js'
import Naming from './routes/Naming.js'
import server from './servers/data.js'
import local from './servers/data.js'
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'
import BeforeStart from './routes/BeforeStart.js'
import BeforeDashboard from './routes/BeforeDashboard.js'
import DesingImprovement from './routes/DesingImprovement';
import Loading from "./Loading";
import CustomSwitch from './CustomSwitch';

// _______________________________________________________________________________________________________________________ //
function App() {
  let origin = ''
  if (window.navigator.userAgent.indexOf('Mac') > 0){
      origin = local['local']
  } else if (window.navigator.userAgent.indexOf('Linux') > 0){
      origin = server['server']    
  }
  // _______________________________________________________________________________________________________________________ //
  
  // log collection
  const [freeLevel, setFreeLevel] = React.useState(1);
  // /cat-attr
  const [attributedTC, setAttributeTC] = useState(0)
  const [brandTC, setBrandTC] = useState(0)
  const [urlTC, setUrlTC] = useState(0)
  // /cluster
  const [selectTC, setSelectTC] = useState(0)
  const [clusterTC, setClusterTC] = useState(0)
  const [clusterNumTC, setClusterNumTC] = useState(0)
  const [xClickTC, setXClickTC] = useState(0)
  const [xUnclickTC, setXUnclickTC] = useState(0)
  // /naming
  const [confirmTC, setConfirmTC] = useState(0)


  let [selectedCatAttr, setselectedCatAttr] = useState([])
  let [clusterNum, setClusterNum] = useState( freeLevel > 0 ?20 : 15 );
  const [phase, setPhased] = useState('image-generation')
  const years = [21, 22, 23];
  const seasons = ['SS', 'FW'];
  const [ys, ChangeYSColor] = useState(Object);
  const [userName, setUserName] = useState('');
  //FIXME : To keep the value you selected
  const [selectedYs, setSelectedYs] = useState('23FW');
  let [styleUrl, setStyleUrl] = useState('')
  let [brandUrl, setBrandUrl] = useState('')
  let [brandSelect, setBrandSelect] = useState('')
  let [finalCount, setFinalCount] = useState(0)
  let [clusterCount, setClusterCount] = useState(0)
  const location2 = useLocation();
  let [method, setMethod] = useState('K-means')
  let [naming, setNaming] = useState({
    Style0 :
      {
          images : ['S_22_anrealage_15.jpg', 'S_22_noir-kei-ninomiya_9.jpg', 'S_22_antonio-marras_55.jpg', 'S_22_cynthia-rowley_20.jpg', 'S_22_threeasfour_16.jpg', 'S_22_adam-lippes_13.jpg', 'S_22_sea_34.jpg', 'S_22_marques-almeida_23.jpg', 'S_22_mame-kurogouchi_25.jpg', 'S_22_rodarte_8.jpg', 'S_22_melitta-baumeister_27.jpg', 'S_22_j-crew_28.jpg', 'S_22_christian-dior_53.jpg', 'S_22_jil-sander_23.jpg', 'S_22_rodarte_63.jpg'],
          status : true    
      },
    Style1 :
      {
          images : ['S_22_noir-kei-ninomiya_9.jpg', 'S_22_noir-kei-ninomiya_9.jpg', 'S_22_antonio-marras_55.jpg', 'S_22_cynthia-rowley_20.jpg', 'S_22_threeasfour_16.jpg', 'S_22_adam-lippes_13.jpg', 'S_22_sea_34.jpg', 'S_22_marques-almeida_23.jpg', 'S_22_mame-kurogouchi_25.jpg', 'S_22_rodarte_8.jpg', 'S_22_melitta-baumeister_27.jpg', 'S_22_j-crew_28.jpg', 'S_22_christian-dior_53.jpg', 'S_22_jil-sander_23.jpg', 'S_22_rodarte_63.jpg'],
          status : false                         
      }
  })
  let [cluster, setCluster] = useState({
    'K-means' : {
      [`k${clusterNum}`] : {
        'cluster0' : {
            'status': false,
            'image': [
                '123',
                '123',
            ],                 
          }
      }
    },
    'GMM': {
      [`k${clusterNum}`]: {
          'cluster0' : {
              'status': false,
              'image': [
                  '123',
                  '123',
              ],
          }
      }
  }
})

let [category, setCategory] = useState({
  'T-shirt': {
    'T-shirt' : {
      'status': false,
      'free':0
      }
    }
  });

const [color, setColor] = useState({
  'color': {
      'category': [
          [{'index': 2, 'id': 'vivid', 'name': 'vivid', 'free':1}], 
          [{'index': 2, 'id': 'vivid', 'name': 'vivid', 'free':1}], 
          [{'index': 9, 'id':'pale', 'name': 'pale', 'free':0}], 
          [{'index': 24, 'id': 'mute', 'name': 'mute', 'free':0}]
      ], 
      'attribute': [
          [{'index': 1, 'id': 'blue', 'name': 'blue', 'rgb':"rgb(100,200,100)", 'free':1}],
          [{'index': 2, 'id': 'blue2', 'name': 'blue2','rgb':"rgb(100,200,100)", 'free':1}],
          [{'index': 2, 'id': 'pink', 'name': 'pink','rgb':"rgb(100,200,100)", 'free':0}],
          [{'index': 2, 'id': 'gray', 'name': 'gray','rgb':"rgb(100,200,100)", 'free':0}],
      ]
  }
})

const [loading, setLoading] = useState(false)

    useEffect(()=>{
      //axios call intercept
      axios.interceptors.request.use(function (config) {
        setLoading(true)
        return config
      }, function (error) {
        return Promise.reject(error);
      });
      //Intercept at the end of an axios call
      axios.interceptors.response.use(function (response) {      
        setLoading(false)
        return response;
      }, function (error) {
        setLoading(false)
        return Promise.reject(error);
      });
    },[]);

    // Receiving user input when the Go button is pressed
  const handleInputChange = (e, type) => {
    if (type === 'imageUrl'){
        setStyleUrl(e.target.value)
    }   
    if (type === 'brandUrl'){
        setBrandUrl(e.target.value)
    }     
    if (type === 'brandSelect'){
        setBrandSelect(e.target.value)
    }
    if (type === 'userName') {
        window.user = e.target.value
        setUserName(e.target.value)
    }
  }
  
  const url = origin;

  const handleSliderChange = (event, newValue) => {
    setFreeLevel(newValue);
    setClusterNum(freeLevel > 0 ? 20 :15)
  };

  const handelSwitchChange = () => {
    let newLevel = 0
    if(freeLevel === 0){
      newLevel = 1
    } else {
      newLevel = 0
    }
    setFreeLevel(newLevel)
 
    // Leave a log
    let localhost = origin +'api'
    let url = localhost + '/toggle'
    let array = {
      'toggle' :{
        'page': location2.pathname,
        'original_status' : freeLevel,
        'status' : freeLevel === 0 ? 1 : 0,
      },
      'season': window.season
    }

    let form = new FormData();
    form.append('log', JSON.stringify(array))
    axios.post(url , form
      ).then(async(res)=>{
      }).catch((err)=>{
    })
  }
  
  return (
    <div className="App">
          <DndProvider backend={HTML5Backend}>  
            <Grid style={{ display : ['/cat-attr', '/cluster', '/naming', '/design-improvement'].includes(location2.pathname)  ? 'none' : 'none'}}
              container alignItems="center" justifyContent="center">
              <Typography sx={{ marginRight: 2}} display='inline' >AI </Typography>
              {/* <CustomSlider 
                  onChange={handleSliderChange}
                  defaultValue={0}
                  step={1}
                  min={0}
                  max={1}
              /> */}
              <CustomSwitch {...'123'} defaultChecked
                onChange={(e) => handelSwitchChange()}
                checked={freeLevel} 
              />
            </Grid>

          <Nav confirmTC={confirmTC} setConfirmTC={setConfirmTC} selectTC={selectTC} clusterTC={clusterTC} clusterNumTC={clusterNumTC} xClickTC={xClickTC} xUnclickTC={xUnclickTC} attributedTC={attributedTC} urlTC={urlTC} brandTC={brandTC} origin={origin} phase={phase} color={color} clusterCount={clusterCount} finalCount={finalCount} naming={naming} userName={userName} handleInputChange={handleInputChange} cluster={cluster} clusterNum={clusterNum} category={category} selectedYs={selectedYs} location={location2} freeLevel={freeLevel}>
          </Nav> 
            <Routes ys={selectedYs}>
              <Route path="/" element={<BeforeStart />}/>
              <Route path="/start" element={<div><MenuStart ChangeYSColor={ChangeYSColor} setSelectedYs={setSelectedYs} selectedYs={selectedYs} years={years} seasons={seasons} ys={ys} url={url}/></div>}/>
              <Route path="/cat-attr" element={<CatAttr attributedTC={attributedTC} setAttributeTC={setAttributeTC} urlTC={urlTC} setUrlTC={setUrlTC} brandTC={brandTC} setBrandTC={setBrandTC} color={color} setColor={setColor} finalCount={finalCount} setFinalCount={setFinalCount} ys={selectedYs} styleUrl={styleUrl} brandUrl={brandUrl} brandSelect={brandSelect} handleInputChange={handleInputChange} setselectedCatAttr={setselectedCatAttr} freeLevel={freeLevel} selectedCatAttr={selectedCatAttr} category={category} setCategory={setCategory}/>}/>
              <Route path="/cluster" element={<Cluster setSelectTC={setSelectTC} setClusterTC={setClusterTC} setClusterNumTC={setClusterNumTC} selectTC={selectTC} xUnclickTC={xUnclickTC} xClickTC={xClickTC} clusterTC={clusterTC} setXClickTC={setXClickTC} setXUnclickTC={setXUnclickTC} clusterNumTC={clusterNumTC} setClusterCount={setClusterCount} clusterCount={clusterCount} setMethod={setMethod} method={method} cluster={cluster} setCluster={setCluster} clusterNum={clusterNum} setClusterNum={setClusterNum} category={category} freeLevel={freeLevel}/>}/>
              <Route path="/naming" element={<Naming setConfirmTC={setConfirmTC} confirmTC={confirmTC} naming={naming} setNaming={setNaming} clusterNum={clusterNum} setClusterNum={setClusterNum} category={category} freeLevel={freeLevel}/>}/> 
              <Route path='/before-dashboard' element={<BeforeDashboard /> }/>
              <Route path='/design-improvement' element={<DesingImprovement setFreeLevel={setFreeLevel} phase={phase} setPhased={setPhased} freeLevel={freeLevel} />}/>
            </Routes>
          </DndProvider> 
          <Loading loading={loading}/>
    </div>
  );
}

function Nav(props){

  const [loading, setLoading] = useState(null)
  let navigate = useNavigate()
  let nextPage = {
    '/' : '/start',
    '/start' : '/cat-attr',
    '/cat-attr' : '/cluster',
    '/cluster' : '/naming',
    '/naming' : '/before-dashboard',
    '/before-dashboard' : '/design-improvement',
    '/design-improvement' : '/imgae-generation'
  };

  let navContent = {
    '/' : '\n\n\n\n\nWelcome to CoCoStyle! \n\nCoCoStyle is an AI based interface for fashion designers.\n\n \n\n \n\n\n',
    '/start' : 'Let’s start with the CoResearch step!',
    '/cat-attr' : props.freeLevel === 0 ? ' This is the second step of trend analysis. These are fashion details extracted by artificial intelligence from the selected season.\n If you select no freedom, you can proceed to the next step by receiving recommended trend details for this season.\n If you select with freedom, you can directly select the details needed for trend analysis. There are.\nIf you select more than 200, you can receive recommended results with higher accuracy in the next step.':"",
    '/cluster' : props.freeLevel === 0 ? 'This is the third step of trend analysis. Artificial intelligence groups together frequently combined details among the details selected in the previous step.\nIf you select no degree of freedom, you can see the trend style recommended by artificial intelligence.\nIf you select with degree of freedom, you can manipulate the artificial intelligence. You can cluster trend styles directly.\nThere are two clustering methodologies, feel free to choose and use the one you want!\nThe recommended number of choices is 10 to 15. ':"",
    '/naming' : props.freeLevel === 0 ? 'Shall we start analyzing based on the trend style recommended by artificial intelligence?' : '',
    '/before-dashboard' : ' You have completed CoResearch. Lets’s move on?    ',
    '/design-improvement' : props.phase === 'design-improvement' ?'If you select No Degree of Freedom, you can receive trend scores and improvement recommendations for your design.\n If you choose Having Freedom, you can receive trend scores and improvement recommendations for your design in two ways.' : 'If you select No Degree of Freedom, you can receive random image creation for the style.\nIf you select With Degree of Freedom, you can freely manipulate random images.'
  };


  let btnStartLabel = ['/'].includes(props.location.pathname)  ? 'Start' : 'Next'
  let category_json = JSON.stringify(props.category)
  let cluster_json = JSON.stringify(props.cluster)

  let corlor_json = JSON.stringify(props.color)
  let localhost = props.origin +'api'

  const handleStartOnclick = (e) => {
    let url = localhost + '/start'
    let form = new FormData();
    form.append('user_name', JSON.stringify(props.userName))
    form.append('free', JSON.stringify(props.freeLevel))

    axios.post(url , form
      ).then(async(res)=>{
      }).catch((err)=>{
    })

    navigate(nextPage[props.location.pathname],{
      state: window.ys
      
    })
  }

  const activeEnter = (e) => {
    if (e.key === 'Enter' && e.nativeEvent.isComposing === false) {
      handleStartOnclick(e); // Click event is executed when Enter is input.
    }
  }

  return (
    <div style={{ display : ['/design-improvement'].includes(props.location.pathname)  ? 'none' : 'block'}}>
      <div className='nav' >
        <div className='custom-btn back-button' style={{ visibility : ['/', '/start', '/before-dashboard', '/design-improvement'].includes(props.location.pathname)  ? 'hidden' : 'visible'}}>
            <Button onClick={(e)=>{ 
              navigate(-1)
              }} size='lg'>
              Back
            </Button></div>
          <div className='nav-title'>
          {
            ['/'].includes(props.location.pathname)  ? 'CoCoStyle' : ''
          }
          {
            ['/start', '/cat-attr', '/cluster', '/naming', '/before-dashboard'].includes(props.location.pathname) ? 'CoResearch' : ''
          }</div>
          <div className='custom-btn start-button' style={{ visibility : ['/', '/before-dashboard', '/design-improvement'].includes(props.location.pathname)  ? 'hidden' : 'visible'}}>
            <Button onClick={async(e)=>{ 
              let form = new FormData()
              let num = /\d+/g
              let str = /[A-Z]+/g

              window.ys = '23FW'
              window.season = 'FW'

              // let year2  = num.exec(window.ys)[0]
              // let season2 = str.exec(window.ys)[0]
              let year2 = '23'
              let season2 = 'FW'
              let array = {
                'clicked' : {
                  'attribute' : props.attributedTC,
                  'url_go' : props.urlTC,
                  'brand_go' : props.brandTC
                },
                'season' : window.season
              }

              form.append('ys', JSON.stringify('20' + year2 + season2))
              form.append('category', category_json)
              form.append('cluster', cluster_json)
              form.append('cluster_num', props.clusterNum) 
              form.append('test', JSON.stringify('test'))
              form.append('color', corlor_json)
              form.append('log', JSON.stringify(array))
 
              if ( props.freeLevel === 0 ){
                form.append('method', JSON.stringify('K-means'))
              } else {
                form.append('method', JSON.stringify('GMM')) 
              }
              
              let response = []
              let params = '20' + year2 + season2
              let api = nextPage[props.location.pathname]
              let url = ''

              if ( props.location.pathname === '/start' ){ 
                url = localhost + api + '/' + params + '/attr'
              } else if ( props.location.pathname === '/naming' ){
                url = localhost + '/naming' + '/' + params + '/save' 
              } else if (props.location.pathname === '/before-dashboard') {
                url = localhost + '/ds' + '/url'
              } else { 
                url = localhost + api
              }

              //api/naming/<ys>/save'
              if ( props.location.pathname === '/naming' ){ 
                //log
                //FIXME : Naming log
                props.naming['log'] = {
                  'clicked' : {
                      'confirm' :  props.confirmTC
                  },
                  'season' : window.season 
                }
                let naming_json = JSON.stringify(props.naming)
                form = new FormData()
                form = naming_json
              } 

              if ( props.location.pathname === '/cluster' ){ 
                let arrayCluster = {
                  'clicked' :{
                    'select' : props.selectTC,
                    'cluster' : props.clusterTC,
                    'cluster_num' : props.clusterNumTC,
                    'x_click' : props.xClickTC,
                    'x_unclick' : props.xUnclickTC
                  }
                }
                form = new FormData()
                form.append('methods',cluster_json)
                form.append('ys', JSON.stringify('20' + year2 + season2))
                form.append('free', JSON.stringify(props.freeLevel))
                form.append('log', JSON.stringify(arrayCluster))
              } 
             await axios.post(url , form
                ).then(async(res)=>{
                  if (res.data === null) {
                    navigate(nextPage[props.location.pathname],{
                    })
                  } else {
                    navigate(nextPage[props.location.pathname],{
                      state:  {
                        common_attributes : res.data['common_attributes'],
                        category : category_json,
                        cat_attr : res.data['cat_attr'], 
                        cluster : res.data, 
                      
                      }
                    })
                  }

                  
                }).catch((err)=>{
                })              
            }} size='lg'disabled={(props.finalCount === 0 && ['', '/cat-attr'].includes(props.location.pathname)) 
            || props.clusterCount === 0 && props.freeLevel > 0 && ['', '/cluster'].includes(props.location.pathname) ? true : false }>{btnStartLabel}</Button></div>
      </div>
      <div className='nav-content' > {  navContent[props.location.pathname]} 
        <div className='user-name' style={{ display : ['/'].includes(props.location.pathname)  ? 'flex' : 'none'}}>
          <input className='user-input' style={{ display : ['/'].includes(props.location.pathname)  ? 'flex' : 'none'}} onKeyDown={(e) => activeEnter(e)} onChange={(e)=> props.handleInputChange(e, 'userName')} placeholder="User name"></input>
          <div className='custom-btn content-start-button' style={{ visibility : ['/'].includes(props.location.pathname)  ? 'visible' : 'hidden'}}>
              <Button onClick={(e)=>{ handleStartOnclick(e)}} size='lg'>{btnStartLabel}</Button>
              </div>
        </div>
        </div>
      </div>
      
    
  )
 
}
export default App;

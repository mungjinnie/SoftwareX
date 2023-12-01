import AWS from 'aws-sdk';
import {useState, useRef, useEffect} from "react";
import {credentials} from './ququ.config.js'
import axios from 'axios'
import server from './servers/data.js'
import local from './servers/data.js'

AWS.config.update({
    accessKeyId: credentials.ACCESS_KEY,
    secretAccessKey: credentials.SECRET_ACCESS_KEY
  });
  

const myBucket = new AWS.S3({
    params: { Bucket: credentials.S3_BUCKET},
    region: credentials.REGION,
  });
  

  export default function S3Upload(props) {
    let origin = ''
    if (window.navigator.userAgent.indexOf('Mac') > 0){
        origin = local['local']
    } else if (window.navigator.userAgent.indexOf('Linux') > 0){
        origin = server['server']  
    }
    const [progress , setProgress] = useState(0);
    const [stopMix1, setStopMix1] = useState(false)
    const [stopMix2, setStopMix2] = useState(false)
    const [stopMix3, setStopMix3] = useState(false)
    const [stopMix4, setStopMix4] = useState(false)
    const [useBucketMix1, setUseBucketMix1] = useState(false)
    const [useBucketMix2, setUseBucketMix2] = useState(false)
    const [useBucketMix3, setUseBucketMix3] = useState(false)
    const [useBucketMix4, setUseBucketMix4] = useState(false)
 
    const [stopInter1, setStopInter1] = useState(false)
    const [stopInter2, setStopInter2] = useState(false)
    const [useBucketInter1, setUseBucketInter1] = useState(false)
    const [useBucketInter2, setUseBucketInter2] = useState(false)
 
    const [stopAttr1, setStopAttr1] = useState(false)
    const [useBucketAttr1, setUseBucketAttr1] = useState(false)
 

    const [showAlert, setShowAlert] = useState(false);
    const fileInputRef = useRef(); 
    
    const [srcs, setSrcs] = useState("https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/upload/default.png" )

    const handleFileInput = (e) => {
        const file = e.target.files[0];
        setProgress(0);
        props.setSelectedFile(e.target.files[0]);

        if (file !== undefined){
            uploadFile(file)
        }
    }

    useEffect(()=>{
      props.setSelectedFile(srcs)
    }, [srcs])
    
const uploadFile = (file) => {  
    let file_name = file.name
    const params = {
        ACL: 'public-read',
        Body: file,
        Bucket: credentials.S3_BUCKET,
        Key: "upload/" + file_name
    };
    
    myBucket.putObject(params)
        .on('httpUploadProgress', (evt) => {
            setProgress(Math.round((evt.loaded / evt.total) * 100))
            setShowAlert(true);
        }).send( async () => {
            await props.setIsUploaded(props.isUploaded + 1)
            let file_url = 'https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/upload/' + file.name
            setSrcs(file_url)
            props.setSelectedFile(file_url)
           
            let localhost = origin+'api'
            let url = localhost + '/ds/url'
            let form = new FormData();

            form.append('url',JSON.stringify(file_url))
            form.append('free', JSON.stringify('0'))

            if (props.type === 'user-target'){
                axios.post(url , form
                 ).then(async(res)=>{
                    let tmp = res.data
                    props.setImproveAttr(JSON.parse(tmp)['target_style'])
                    props.setLabelingResult(JSON.parse(tmp)) 
                    let key = Object.keys(JSON.parse(tmp)['target_style'])[0]                    
                    props.setSelectedStyle(JSON.parse(tmp)['target_style'][key]['style'])  
                    props.setUploadTC(props.uploadTC + 1)       
                }).catch((err)=>{

                })
            } else if (props.type === 'style-mixing'){

                if (props.mixtype === 1){
                    setUseBucketMix1(true)
                    props.array['info']['0'] = {}
                    props.array['info']['0']['diversity'] = 0
                    props.array['info']['0']['quality'] = 0
                    props.array['info']['0']['style'] = 'none'
                    props.array['info']['0']['number'] = 0
                    props.array['info']['0']['url'] = file_url
    
                }
                if (props.mixtype === 2){
                    setUseBucketMix2(true)
                    props.array['info']['1'] = {}
                    props.array['info']['1']['diversity'] = 0
                    props.array['info']['1']['quality'] = 0
                    props.array['info']['1']['style'] = 'none'
                    props.array['info']['1']['number'] = 0
                    props.array['info']['1']['url'] = file_url

                }
                if (props.mixtype === 3){
                    setUseBucketMix3(true)
                    props.array['info']['2'] = {}
                    props.array['info']['2']['diversity'] = 0
                    props.array['info']['2']['quality'] = 0
                    props.array['info']['2']['style'] = 'none'
                    props.array['info']['2']['number'] = 0
                    props.array['info']['2']['url'] = file_url

                }
                if (props.mixtype === 4){
                    setUseBucketMix4(true)
                    props.array['info']['3'] = {}
                    props.array['info']['3']['diversity'] = 0
                    props.array['info']['3']['quality'] = 0
                    props.array['info']['3']['style'] = 'none'
                    props.array['info']['3']['number'] = 0
                    props.array['info']['3']['url'] = file_url

                }
                props.setGanUploadMixTC(props.ganUploadMixTC + 1) 

            } else if (props.type === 'interpolation'){
                if (props.intertype === 1){
                    setUseBucketInter1(true)
                    props.array['info']['0'] = {}
                    props.array['info']['0']['diversity'] = 0
                    props.array['info']['0']['quality'] = 0
                    props.array['info']['0']['style'] = 'none'
                    props.array['info']['0']['number'] = 0
                    props.array['info']['0']['url'] = file_url

                }
                if (props.intertype === 2){
                    setUseBucketInter2(true)
                    props.array['info']['1'] = {}
                    props.array['info']['1']['diversity'] = 0
                    props.array['info']['1']['quality'] = 0
                    props.array['info']['1']['style'] = 'none'
                    props.array['info']['1']['number'] = 0
                    props.array['info']['1']['url'] = file_url

                }
                props.setGanUploadInterTC(props.ganUploadInterTC + 1) 
            } else if (props.type === 'attributeedit'){
                if (props.attrtype === 1){
                    setUseBucketAttr1(true)
                    props.array['info']['0'] = {}
                    props.array['info']['0']['diversity'] = 0
                    props.array['info']['0']['quality'] = 0
                    props.array['info']['0']['style'] = 'none'
                    props.array['info']['0']['number'] = 0
                    props.array['info']['0']['url'] = file_url
                }
                props.setGanUploadAttrTC(props.ganUploadAttrTC + 1) 
            }
        })
    }
    
    if ((stopMix1 === false)&& props.isUploaded.length > 1){
        setSrcs(props.isUploaded)
        setStopMix1(true)
        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div className='my-style-file-text1'>&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )

    } else if ((stopMix2 === false && props.isUploaded.length > 1)) {
        setSrcs(props.isUploaded)
        setStopMix2(true)

        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div className='my-style-file-text1'>&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )

    }else if ((stopMix3 === false && props.isUploaded.length > 1)) {
        setSrcs(props.isUploaded)
        setStopMix3(true)

        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div className='my-style-file-text1'>&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )

    } else if ((stopMix4 === false && props.isUploaded.length > 1)){
        setSrcs(props.isUploaded)
        setStopMix4(true)

        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div className='my-style-file-text1'>&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )
    }else if ((stopInter1 === false && props.isUploaded.length > 1)){
        setSrcs(props.isUploaded)
        setStopInter1(true)

        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div className='my-style-file-text1'>&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )
    }else if ((stopInter2 === false && props.isUploaded.length > 1)){
        setSrcs(props.isUploaded)
        setStopInter2(true)

        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div className='my-style-file-text1'>&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )
    }else if ((stopAttr1 === false && props.isUploaded.length > 1)){
        setSrcs(props.isUploaded)
        setStopAttr1(true)

        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div className='my-style-file-text1'>&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )
    }else  {
        return (
            <div className={`${props.type === 'user-target' ? 'my-style-parent-container': 'my-gan-parent-container'}`} onClick={()=>{
                fileInputRef.current.click()
            }}  >
                <input  disabled={props.type2 == 'improve' ? false : true} className='input-file' ref={fileInputRef} type="file" id="file" onChange={handleFileInput} multiple="multiple" hidden/>
                <div className={`${props.type === 'user-target' ? 'my-style-file-container': 'my-gan-file-container'}`} 
                    style={{ display : props.isUploaded === 0  ? 'flex' : 'none'}}>
                    <div style={{display: props.type2 == 'improve' ? "block" : "none"}}  className='my-style-file-text1'>Upload&nbsp;</div>
                    <div className='my-style-file-text2'></div>
                </div>
                <img className='my-style-file-img' style={{ display : props.isUploaded > 0 || props.isUploaded.length > 1  ? 'flex' : 'none'}} src={srcs}/>
            </div>
        )
    }




    
}

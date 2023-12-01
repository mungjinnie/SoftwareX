import React, { useEffect, useState } from "react";
import LazyLoad from 'react-lazyload';

//cluster-images
function CustomClusterImages3(props) {
    let [arr, setArr] = useState([])
    let emptyArr = [];
    let tmp4 = [];
    useEffect(()=>{
        setArr(emptyArr);
    }, [])
    let tmp = [];

    let imageArr = props.info['info']
    if (imageArr === undefined ){
        return 
    }
    return (
        <>
        {               
            imageArr.map((image, ii) => {
                let srcs = image['url']
                return (
                    <div className='lazy-class2'>
                    <LazyLoad key={ii} once>
                        
                            <div className={'cluster-images'}>
                                {
                                    props.class === 'cluster-hover' ? (
                                        <img className="hue-images" src={srcs} alt={`Image ${ii}`} />
                                    ) : (
                                        <img className="hue-images" src={srcs} alt={`Image ${ii}`} />
                                )}    
                            </div>
                        
                        {
                            props.freeLevel === 1 ? <div>{ii}</div> : <div></div>  
                        }
                    </LazyLoad>
                    </div>
                    )
            })
        }
          </>
    )
}
export default  CustomClusterImages3;
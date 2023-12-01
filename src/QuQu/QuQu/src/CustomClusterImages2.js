import React, { useEffect, useState } from "react";
import LazyLoad from 'react-lazyload';

//cluster-images
function CustomClusterImages2(props) {
    let [arr, setArr] = useState([])
    let emptyArr = [];
    let tmp4 = [];
    useEffect(()=>{
        setArr(emptyArr);
    }, [])
    let tmp = [];
    let imageArr = props.naming[props.style]
    let prefix_src = 'https://ququ-bucket.s3.ap-northeast-2.amazonaws.com/fw_2023/'
    if (imageArr === undefined ){
        return 
    }
    return (
        <>

        {               
            imageArr['images'].map((image, ii) => {
                let srcs = prefix_src + image
                return (
                    <div className='lazy-class2'>
                    <LazyLoad once>
                    <div className={'cluster-images-box'}>
                            <div className={'cluster-images'}>
                            {
                                props.class === 'cluster-hover' ? (
                                    <img src={srcs} alt={`Image ${ii}`} />
                                ) : (
                                    <img src={srcs} alt={`Image ${ii}`} />
                                )}
                        </div>
                    </div>
                    </LazyLoad>
                    </div>
                    )
            })
        }
          </>
    )
}
export default  CustomClusterImages2;
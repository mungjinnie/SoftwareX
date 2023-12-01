import { styled } from '@mui/material/styles';
import Slider from '@mui/material/Slider';

const QuQuSlider = styled(Slider)({
    color: 'rgb(196, 198, 251)',
    width:'35%',
    '& .MuiSlider-track': {
      border: 'none',
    },
    '& .MuiSlider-thumb': {
      height: 15,
      width: 15,
      backgroundColor: '#fff',
      border: '2px solid currentColor',
      '&:focus, &:hover, &.Mui-active, &.Mui-focusVisible': {
        boxShadow: 'inherit',
      },
    },
  });
export default  QuQuSlider;
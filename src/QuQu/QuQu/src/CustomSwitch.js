
import { styled } from '@mui/material/styles';
import Switch, { SwitchProps } from '@mui/material/Switch';


const CustomSwitch = styled(Switch)(({ theme }) => ({
    width: 60,
    height: 34,
    padding: 8,
    '& .MuiSwitch-switchBase': {
      padding: 0,
      margin: 5,
      transform: 'translateX(3px)',
      '&.Mui-checked': {
        color: '#fff',
        transform: 'translateX(30px)',
        '& .MuiSwitch-thumb:before': {
        },
        '& + .MuiSwitch-track': {
          opacity: 1,
          backgroundColor: theme.palette.mode === 'dark' ? 'rgb(196, 198, 251)' : 'rgb(196, 198, 251)',
        },
      },
    },
    '& .MuiSwitch-thumb': {
      backgroundColor: theme.palette.mode === 'dark' ? 'rgb(196, 198, 251)' : 'rgb(196, 198, 251)',
      width: 22,
      height: 22,
      '&:before': {
        content: "''",
        position: 'absolute',
        width: '100%',
        height: '100%',

        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
     },
    },
    '& .MuiSwitch-track': {
      opacity: 1,
      backgroundColor: theme.palette.mode === 'dark' ? 'rgb(196, 198, 251)' : 'rgb(97 106 120)',
      borderRadius: 20,
    },
  }));

export default  CustomSwitch;
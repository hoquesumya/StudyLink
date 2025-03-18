import {configureStore} from '@reduxjs/toolkit'
import loginSlice from './features/loginSlice'
import groupSlice from './features/groupSlice'
import courseSlice from './features/courseSlice'


const store = configureStore({
    reducer: {
        login: loginSlice,
        group: groupSlice,
        course: courseSlice,
    }, 
})

export default store

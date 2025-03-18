import {createSlice} from '@reduxjs/toolkit'

const initialState = {
    courses: [],
    appUsers: [],
}

const courseSlice = createSlice({
    name: 'course',
    initialState: initialState,
    reducers: {
        setCourses: (state, action) => {
            state.courses = action.payload;
        },
        setAppUsers: (state, action) => {
            state.appUsers = action.payload;
        }
    }
})

export const {
    setCourses,
    setAppUsers,
} = courseSlice.actions

export default courseSlice.reducer;

import {createSlice} from '@reduxjs/toolkit'

const initialState = {
    isLoggedIn: false,
    loggedUser: null,
}

const loginSlice = createSlice({
    name: 'login',
    initialState: initialState,
    reducers: {
        login: (state, action) => {
            state.isLoggedIn = true;
            state.loggedUser = action.payload;
        },
        logout: (state, action) => {
            state.isLoggedIn = false;
            state.loggedUser = null;
            localStorage.removeItem('user');
        }
    }
})

export const {
    login,
    logout,
} = loginSlice.actions

export default loginSlice.reducer;
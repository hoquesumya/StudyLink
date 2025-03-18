import {createSlice} from '@reduxjs/toolkit'

const initialState = {
    groups: [],
}

const groupSlice = createSlice({
    name: 'group',
    initialState: initialState,
    reducers: {
        setGroups: (state, action) => {
            state.groups = action.payload;
        },
        addGroup: (state, action) => {
            state.groups = [...state.groups, action.payload];
        },
        deleteGroup: (state, action) => {
            state.groups = state.groups.filter(group => group.group_id !== action.payload);
        },
        updateGroup: (state, action) => {
            state.groups = state.groups.map(group => group.group_id === action.payload.group_id ? action.payload : group);
        },
    }
})

export const {
    setGroups,
    addGroup,
    deleteGroup,
    updateGroup
} = groupSlice.actions

export default groupSlice.reducer;
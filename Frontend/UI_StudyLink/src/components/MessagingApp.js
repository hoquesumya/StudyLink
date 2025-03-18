import React, { useState, useRef, useEffect } from 'react';
import './MessagingApp.css';
import { useSelector, useDispatch } from 'react-redux';
import { setAppUsers } from '../redux/features/courseSlice';

const MessagingApp = ({ initialUser }) => {
  const [conversations, setConversations] = useState([]);
  const [allFetchedConversations, setAllFetchedConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [message, setMessage] = useState('');
  const [showNewChatModal, setShowNewChatModal] = useState(false);
  const [appUsers, setUsers] = useState([]);
  const messageListRef = useRef(null);
  const loggedUser = useSelector(state => state.login.loggedUser) || JSON.parse(localStorage.getItem('user'));
  const [searchQuery, setSearchQuery] = useState('');
  const [fetchedGroups, setFetchedGroups] = useState([]);
  const [searchInGroups, setSearchInGroups] = useState(true);
  const apiBase = process.env.REACT_APP_API_BASE;
  const apiBaseConversations = process.env.REACT_APP_API_BASE_CONVERSATIONS;
  const dispatch = useDispatch();
  const [contextMenu, setContextMenu] = useState({ visible: false, x: 0, y: 0, conversationId: null });
  const apiBaseGroups = process.env.REACT_APP_API_GROUPS;
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMorePages, setHasMorePages] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const params = new URLSearchParams({
          skip: 0,
          limit: 10,
        });
        const response = await fetch(`${apiBase}/users?${params}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${loggedUser.jwt_token}`,
            'Google-Token': `${loggedUser.credentials}`
          }
        });
        const data = await response.json();
        const allUsers = data.users.filter(user => user.user_id !== loggedUser.user_id)
        const allUsersFormatted = allUsers.map(user => [`${user.first_name} ${user.last_name}`, user.user_id]);
        setUsers(allUsersFormatted);
        dispatch(setAppUsers(allUsersFormatted));
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, []); 

  const scrollToBottom = () => {
    messageListRef.current?.scrollTo(0, messageListRef.current.scrollHeight);
  };

  useEffect(scrollToBottom, [conversations]);

  useEffect(() => {
    if (initialUser) {
      const existingConversation = conversations.find(conv => conv.name === initialUser);
      if (existingConversation) {
        setSelectedConversation(existingConversation.name);
      } else {
        const newConversation = {
          id: conversations.length + 1,
          name: initialUser,
          messages: []
        };
        setConversations([newConversation, ...conversations]);
        setSelectedConversation(newConversation.name);
      }
    }
  }, [initialUser]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (message.trim() !== '' && selectedConversation) {
      const newMessage = { text: message, sender: loggedUser.user_id, timestamp: new Date().toLocaleTimeString() };

      const updatedConversations = conversations.map(conv => {
        if (conv.name === selectedConversation) {
          const updatedMessages = [...conv.messages, newMessage];
          updateConversationOnServer(selectedConversation, updatedMessages);
          return { ...conv, messages: updatedMessages };
        }
        return conv;
      });
      setConversations(updatedConversations);
      setMessage('');
    }
  };

  const updateConversationOnServer = async (conversationName, updatedMessages) => {
    let conversation;
    try {
      const response = await fetch(`${apiBaseConversations}/conversations/?page=1&limit=10000000`);
      const data = await response.json();
      console.log('data', data)
      const conversationsData = Array.isArray(data.detail) ? data.detail : [data.detail];
      const formattedConversations = conversationsData.map(convo => {
        const participants = convo.participants ? JSON.parse(convo.participants) : [];
        const messages = convo.messages ? JSON.parse(convo.messages) : [];
        return {
          id: convo.convo_id,
          name: convo.name,
          participants,
          messages,
          isGroup: Boolean(convo.isGroup)
        };
      });
      console.log('conversationsData', conversationsData)
      console.log('formattedConversations', formattedConversations)
      conversation = formattedConversations.find(conv => conv.name === conversationName);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
    console.log('conversation', conversation)
    const url = `${apiBaseConversations}/${loggedUser.user_id}/conversations/${conversation.id}`;

    try {
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${loggedUser.jwt_token}`,
          'Google-Token': `${loggedUser.credentials}`
        },
        body: JSON.stringify({
          name: conversation.name,
          participants: conversation.participants,
          messages: updatedMessages,
          isGroup: conversation.isGroup
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update conversation');
      }

      console.log('Conversation updated successfully');
    } catch (error) {
      console.error('Error updating conversation:', error);
    }
  };

  const startNewChat = async (conversationName, userId=null, isGroup = false) => {
    console.log('conversations', conversations)
    if(conversations.length >0) {
      setCurrentPage(currentPage + 1);
    }
    let existingConversation;  
    if (isGroup) {
      existingConversation = conversations.find(conv => conv.name === conversationName && conv.isGroup);
    } else {
      existingConversation = conversations.find(conv => 
        conversationName.split(' - ').includes(conv.participants[0]) && 
        conversationName.split(' - ').includes(conv.participants[1]) && 
        !conv.isGroup
      );
    }

    if (existingConversation) {
      setSelectedConversation(existingConversation.name);
      setShowNewChatModal(false);
      return;
    }

    let newConversation;
    if (isGroup) {
      const group = fetchedGroups.find(g => g.group_name === conversationName);      
      if (!group) {
        console.error('Group not found:', conversationName);
        return;
      }

      newConversation = {
        name: group.group_name,
        participants: group.members,
        messages: [],
        isGroup: true
      };
    } else {
      newConversation = {
        name: conversationName,
        participants: [loggedUser.user_id, userId],
        messages: [],
        isGroup: false
      };
    }

    setConversations([newConversation, ...conversations]);
    setSelectedConversation(newConversation.name);
    setShowNewChatModal(false);

    if (!allFetchedConversations.find(conv => conv.name === newConversation.name)) {
      try {
        const response = await fetch(`${apiBaseConversations}/${loggedUser.user_id}/conversations/?page=${currentPage}&limit=10000000`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${loggedUser.jwt_token}`,
            'Google-Token': `${loggedUser.credentials}`
          },
          body: JSON.stringify(newConversation),
        });
        
        if (!response.ok) {
          throw new Error('Failed to create conversation');
        }
      } catch (error) {
        console.error('Error creating new conversation:', error);
      }
    }
  };

  const filteredUsers = appUsers.filter(user =>
    user[0].toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredGroups = fetchedGroups.filter(group =>
    group.group_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  useEffect(() => {
    const fetchGroups = async () => {
      try {
          const response = await fetch(`${apiBaseGroups}/study-group`, {
          headers: {
            'token': loggedUser.canvas_token
          }
        });
        const data = await response.json();
        setFetchedGroups(data.data.filter(group => group.members.includes(loggedUser.user_id)));
      } catch (error) {
        console.error('Error fetching groups:', error);
      }
    };
    fetchGroups();
  }, []);


  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await fetch(`${apiBaseConversations}/conversations/?page=${currentPage}&limit=1`);
        const data = await response.json();

        const conversationsData = Array.isArray(data.detail) ? data.detail : [data.detail];
        const formattedConversations = conversationsData.map(convo => {
          const participants = convo.participants ? JSON.parse(convo.participants) : [];
          const messages = convo.messages ? JSON.parse(convo.messages) : [];
          return {
            id: convo.convo_id,
            name: convo.name,
            participants,
            messages,
            isGroup: Boolean(convo.isGroup)
          };
        });
        const filteredConversations = formattedConversations.filter(convo => 
          convo.participants.includes(loggedUser.user_id)
        );
        setConversations(filteredConversations);
        setAllFetchedConversations(formattedConversations);
        const response2 = await fetch(`${apiBaseConversations}/conversations/?page=${currentPage+1}&limit=1`);
        const data2 = await response2.json();
        setHasMorePages(data2.detail.length > 0);
      } catch (error) {
        console.error('Error fetching conversations:', error);
      }
    };

    fetchConversations();

    const intervalId = setInterval(fetchConversations, 1000);
    return () => clearInterval(intervalId);
  }, [currentPage, apiBaseConversations,loggedUser.user_id]); 

  const handleNextPage = () => {
    if (hasMorePages) {
      setCurrentPage(prev => prev + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(prev => prev - 1);
      setHasMorePages(true);
    }
  };

  const handleDeleteConversation = async (conversationId) => {
    try {
      const response = await fetch(`${apiBaseConversations}/${loggedUser.user_id}/conversations/${conversationId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${loggedUser.jwt_token}`,
          'Google-Token': `${loggedUser.credentials}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to delete conversation');
      }
      setConversations(prevConversations => 
        prevConversations.filter(conv => conv.id !== conversationId)
      );
      if (selectedConversation === conversationId) {
        setSelectedConversation(null);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
    
    setContextMenu({ visible: false, x: 0, y: 0, conversationId: null });
  };

  useEffect(() => {
    const handleClickOutside = () => {
      setContextMenu({ visible: false, x: 0, y: 0, conversationId: null });
    };

    if (contextMenu.visible) {
      document.addEventListener('click', handleClickOutside);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [contextMenu.visible]);

  return (
    <div className="messaging-app">
      <div className="conversation-list">
        <div className="conversation-header">
          <h2>Conversations</h2>
        </div>
        <button className="new-chat-button" onClick={() => setShowNewChatModal(true)}>Create New Chat</button>
        {Array.isArray(conversations) && conversations.map((conv) => (
          <div
            key={conv.id}
            className={`conversation-item ${selectedConversation === conv.name ? 'selected' : ''}`}
            onClick={() => setSelectedConversation(conv.name)}
            onContextMenu={(e) => {
              e.preventDefault();
              setContextMenu({
                visible: true,
                x: e.clientX,
                y: e.clientY,
                conversationId: conv.id
              });
            }}
          >
            <h3>{conv.name.split(' - ')[1] === loggedUser.user_id ? conv.name.split(' - ')[2] : conv.name.split(' - ')[0]}</h3>
            <p>{conv.messages[conv.messages.length - 1]?.text || 'No messages yet'}</p>
          </div>
        ))}
        <div className="pagination-controls-container">
          <div className="pagination-controls">
            <button 
            onClick={handlePrevPage} 
            disabled={currentPage === 1}
          >
            Previous Page
          </button>
          <span>Page {currentPage}</span>
          <button 
            onClick={handleNextPage}
            disabled={!hasMorePages}
          >
            Next Page
            </button>
          </div>
        </div>
      </div>
      <div className="chat-window">
        {selectedConversation ? (
          <>
            <div className="conversation-header">
              <h2>
                {conversations.find(conv => conv.name === selectedConversation)?.name.split(' - ')[1] === loggedUser.user_id 
                  ? conversations.find(conv => conv.name === selectedConversation)?.name.split(' - ')[2] 
                  : conversations.find(conv => conv.name === selectedConversation)?.name.split(' - ')[0]}
              </h2>
            </div>
            <div className="message-list" ref={messageListRef}>
              {conversations.find(conv => conv.name === selectedConversation)?.messages?.map((msg, index) => {
                const currentConversation = conversations.find(conv => conv.name === selectedConversation);
                const senderName = appUsers.find(user => user[1] === msg.sender)?.[0] || msg.sender;
                
                return (
                  <div key={index} className={`message ${msg.sender === loggedUser.user_id ? 'sent' : 'received'}`}>
                    <div className="message-content">
                      {currentConversation?.isGroup && senderName !== loggedUser.user_id && (
                        <span className="sender-name">{senderName}</span>
                      )}
                      <p>{msg.text}</p>
                    </div>
                    <span className="timestamp">{msg.timestamp}</span>
                  </div>
                );
              })}
            </div>
            <form onSubmit={handleSendMessage} className="message-input">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
              />
              <button type="submit">Send</button>
            </form>
          </>
        ) : (
          <p style={{ marginLeft: '20px' }}>Select a conversation to start chatting</p>
        )}
      </div>
      {showNewChatModal && (
        <div className="modal">
          <div className="modal-content">
            <h2>Start a New Chat</h2>
            <div className="search-options">
              <input
                type="text"
                placeholder="Search users or groups..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <label>
                <input
                  type="checkbox"
                  checked={searchInGroups}
                  onChange={(e) => setSearchInGroups(e.target.checked)}
                />
                Search only in my groups
              </label>
            </div>
            <div className="user-list-container">
              <ul className="user-list">
                {!searchInGroups && filteredUsers.map((user, index) => (
                  <li key={index} onClick={() => startNewChat(user[0]+ ' - '+ user[1] + ' - ' + loggedUser.first_name + ' ' + loggedUser.last_name+ ' - '+ loggedUser.user_id, user[1], false)}>{user[0]}</li>
                ))}
                {searchInGroups && filteredGroups.map((group, index) => (
                  <li key={index} onClick={() => startNewChat(group.group_name, null, true)}>{group.group_name}</li>
                ))}
              </ul>
            </div>
            <button onClick={() => setShowNewChatModal(false)}>Cancel</button>
          </div>
        </div>
      )}
      {contextMenu.visible && (
        <div 
          className="context-menu"
          style={{
            position: 'fixed',
            top: contextMenu.y,
            left: contextMenu.x,
            zIndex: 1000
          }}
        >
          <button onClick={() => handleDeleteConversation(contextMenu.conversationId)}>
            Delete Conversation
          </button>
        </div>
      )}
    </div>
  );
};

export default MessagingApp;

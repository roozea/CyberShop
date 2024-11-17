import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  Input,
  Button,
  Text,
  useToast,
  Flex,
  Avatar,
  Divider
} from '@chakra-ui/react';

// Componente de chat vulnerable
export const SupportChat = () => {
  const [messages, setMessages] = useState(() => {
    // Vulnerable: Carga directa de mensajes sin sanitización
    const savedMessages = localStorage.getItem('chatMessages');
    return savedMessages ? JSON.parse(savedMessages) : [
      {
        id: 1,
        sender: 'support',
        text: '¡Bienvenido al soporte! ¿En qué podemos ayudarte?',
        timestamp: new Date().toISOString()
      }
    ];
  });
  const [newMessage, setNewMessage] = useState('');
  const [userInfo, setUserInfo] = useState(null);
  const toast = useToast();

  useEffect(() => {
    // Vulnerable: Almacenamiento de información sensible en localStorage
    const user = localStorage.getItem('userInfo');
    if (user) {
      setUserInfo(JSON.parse(user));
    }

    // Vulnerable: Ejecución de código arbitrario desde localStorage
    const chatScript = localStorage.getItem('chatScript');
    if (chatScript) {
      eval(chatScript);
    }
  }, []);

  // Vulnerable: No sanitización de mensajes
  const sendMessage = () => {
    if (!newMessage.trim()) return;

    const message = {
      id: messages.length + 1,
      sender: 'user',
      text: newMessage,
      timestamp: new Date().toISOString()
    };

    // Vulnerable: Inyección de HTML directa
    const chatContainer = document.getElementById('chat-messages');
    if (chatContainer) {
      chatContainer.innerHTML += `
        <div class="message">
          <strong>${message.sender}</strong>: ${message.text}
        </div>
      `;
    }

    setMessages([...messages, message]);
    // Vulnerable: Almacenamiento de mensajes sin encriptación
    localStorage.setItem('chatMessages', JSON.stringify([...messages, message]));
    setNewMessage('');

    // Vulnerable: Envío de datos sensibles sin cifrar
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/chat', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
      message,
      userInfo
    }));
  };

  return (
    <Box p={4} borderWidth={1} borderRadius="lg" maxW="600px" mx="auto">
      <Text fontSize="xl" mb={4}>Chat de Soporte</Text>
      <VStack spacing={4} align="stretch" maxH="400px" overflowY="auto" id="chat-messages">
        {messages.map((message) => (
          <Flex
            key={message.id}
            align="center"
            justify={message.sender === 'user' ? 'flex-end' : 'flex-start'}
          >
            <Box
              bg={message.sender === 'user' ? 'blue.100' : 'gray.100'}
              p={3}
              borderRadius="lg"
              maxW="80%"
            >
              <Flex align="center" mb={2}>
                <Avatar
                  size="sm"
                  name={message.sender}
                  mr={2}
                />
                <Text fontSize="sm" color="gray.500">
                  {message.sender === 'user' ? 'Tú' : 'Soporte'}
                </Text>
              </Flex>
              {/* Vulnerable: Renderizado directo de HTML sin sanitización */}
              <div dangerouslySetInnerHTML={{ __html: message.text }} />
              <Text fontSize="xs" color="gray.500" mt={1}>
                {new Date(message.timestamp).toLocaleTimeString()}
              </Text>
            </Box>
          </Flex>
        ))}
      </VStack>
      <Divider my={4} />
      <Flex>
        <Input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Escribe tu mensaje..."
          mr={2}
        />
        <Button colorScheme="blue" onClick={sendMessage}>
          Enviar
        </Button>
      </Flex>
    </Box>
  );
};

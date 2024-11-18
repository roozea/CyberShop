import { Box, Button, FormControl, FormLabel, Input, VStack, Heading, Text, useToast } from '@chakra-ui/react';
import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { login } from '../services/api';

export const Login = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Vulnerable: No validación de entrada
      const response = await login({
        email: formData.email,
        password: formData.password
      });

      if (response && response.access_token) {
        // Vulnerable: Mensaje revela información
        toast({
          title: 'Inicio de sesión exitoso',
          description: `Bienvenido ${response.user_data.email}`,
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
        navigate('/');
      }
    } catch (error) {
      // Vulnerable: Mensaje de error detallado
      toast({
        title: 'Error de autenticación',
        description: 'Email o contraseña incorrectos',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      console.error('Error de login:', error);
    }
  };

  return (
    <Box maxW="md" mx="auto" mt={8}>
      <VStack spacing={4} align="stretch" as="form" onSubmit={handleLogin}>
        <Heading>Iniciar Sesión</Heading>
        <FormControl>
          <FormLabel>Email</FormLabel>
          <Input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="tu@email.com"
          />
        </FormControl>
        <FormControl>
          <FormLabel>Contraseña</FormLabel>
          <Input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="********"
          />
        </FormControl>
        <Button type="submit" colorScheme="blue">Ingresar</Button>
        <Text>
          ¿No tienes cuenta? <Link to="/register" style={{ color: 'blue' }}>Regístrate aquí</Link>
        </Text>
      </VStack>
    </Box>
  );
};

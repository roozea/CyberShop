import { Box, Button, FormControl, FormLabel, Input, VStack, Heading, Text, useToast } from '@chakra-ui/react';
import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { register } from '../services/api';

export const Register = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    credit_card: '',
    address: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    // Vulnerable: No validación de contraseña
    if (formData.password !== formData.confirmPassword) {
      toast({
        title: 'Error',
        description: 'Las contraseñas no coinciden',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    // Vulnerable: Envío de datos sensibles sin encriptar
    const userData = {
      email: formData.email,
      password: formData.password,
      credit_card: formData.credit_card,
      address: formData.address
    };

    const response = await register(userData);

    if (response) {
      toast({
        title: 'Registro exitoso',
        description: 'Tu cuenta ha sido creada',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      navigate('/login');
    } else {
      toast({
        title: 'Error en el registro',
        description: 'No se pudo crear la cuenta',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box maxW="md" mx="auto" mt={8}>
      <VStack spacing={4} align="stretch" as="form" onSubmit={handleRegister}>
        <Heading>Registro</Heading>
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
        <FormControl>
          <FormLabel>Confirmar Contraseña</FormLabel>
          <Input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder="********"
          />
        </FormControl>
        <FormControl>
          <FormLabel>Tarjeta de Crédito</FormLabel>
          <Input
            type="text"
            name="credit_card"
            value={formData.credit_card}
            onChange={handleChange}
            placeholder="1234-5678-9012-3456"
          />
        </FormControl>
        <FormControl>
          <FormLabel>Dirección</FormLabel>
          <Input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            placeholder="Tu dirección"
          />
        </FormControl>
        <Button type="submit" colorScheme="blue">Registrarse</Button>
        <Text>
          ¿Ya tienes cuenta? <Link to="/login" style={{ color: 'blue' }}>Ingresa aquí</Link>
        </Text>
      </VStack>
    </Box>
  );
};

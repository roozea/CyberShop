import { Box, Button, FormControl, FormLabel, Input, VStack, Heading, Text, useToast } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

export const Login = () => {
  const toast = useToast();

  const handleLogin = (e) => {
    e.preventDefault();
    // Implementación vulnerable intencionalmente (sin validación)
    toast({
      title: 'Inicio de sesión exitoso',
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Box maxW="md" mx="auto" mt={8}>
      <VStack spacing={4} align="stretch" as="form" onSubmit={handleLogin}>
        <Heading>Iniciar Sesión</Heading>
        <FormControl>
          <FormLabel>Email</FormLabel>
          <Input type="email" placeholder="tu@email.com" />
        </FormControl>
        <FormControl>
          <FormLabel>Contraseña</FormLabel>
          <Input type="password" placeholder="********" />
        </FormControl>
        <Button type="submit" colorScheme="blue">Ingresar</Button>
        <Text>
          ¿No tienes cuenta? <Link to="/register" style={{ color: 'blue' }}>Regístrate aquí</Link>
        </Text>
      </VStack>
    </Box>
  );
};

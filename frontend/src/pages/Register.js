import { Box, Button, FormControl, FormLabel, Input, VStack, Heading, Text, useToast } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

export const Register = () => {
  const toast = useToast();

  const handleRegister = (e) => {
    e.preventDefault();
    // Implementación vulnerable intencionalmente (sin validaciones de seguridad)
    toast({
      title: 'Registro exitoso',
      description: 'Tu cuenta ha sido creada',
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Box maxW="md" mx="auto" mt={8}>
      <VStack spacing={4} align="stretch" as="form" onSubmit={handleRegister}>
        <Heading>Registro</Heading>
        <FormControl>
          <FormLabel>Nombre</FormLabel>
          <Input placeholder="Tu nombre" />
        </FormControl>
        <FormControl>
          <FormLabel>Email</FormLabel>
          <Input type="email" placeholder="tu@email.com" />
        </FormControl>
        <FormControl>
          <FormLabel>Contraseña</FormLabel>
          <Input type="password" placeholder="********" />
        </FormControl>
        <FormControl>
          <FormLabel>Confirmar Contraseña</FormLabel>
          <Input type="password" placeholder="********" />
        </FormControl>
        <Button type="submit" colorScheme="blue">Registrarse</Button>
        <Text>
          ¿Ya tienes cuenta? <Link to="/login" style={{ color: 'blue' }}>Ingresa aquí</Link>
        </Text>
      </VStack>
    </Box>
  );
};

import { Box, Flex, Heading, Button, Input, InputGroup, InputRightElement } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

export const Navbar = () => {
  return (
    <Box bg="gray.100" px={4} py={2}>
      <Flex justify="space-between" align="center">
        <Link to="/">
          <Heading size="md">CyberShop</Heading>
        </Link>

        <InputGroup maxW="400px">
          <Input placeholder="Buscar productos..." bg="white" />
          <InputRightElement width="4.5rem">
            <Button h="1.75rem" size="sm">
              Buscar
            </Button>
          </InputRightElement>
        </InputGroup>

        <Flex gap={4}>
          <Link to="/login">
            <Button variant="ghost">Login</Button>
          </Link>
          <Link to="/register">
            <Button variant="ghost">Registro</Button>
          </Link>
          <Link to="/cart">
            <Button colorScheme="blue">Carrito (0)</Button>
          </Link>
        </Flex>
      </Flex>
    </Box>
  );
};

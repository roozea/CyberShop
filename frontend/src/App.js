import React from "react";
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Cart } from './pages/Cart';
import { ProductDetail } from './pages/ProductDetail';
import { WishList } from './components/WishList';
import { ProductComparison } from './components/ProductComparison';
import { OrderHistory } from './components/OrderHistory';
import { SupportChat } from './components/SupportChat';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/product/:id" element={<ProductDetail />} />
          <Route path="/wishlist" element={<WishList />} />
          <Route path="/compare" element={<ProductComparison />} />
          <Route path="/orders" element={<OrderHistory />} />
          <Route path="/support" element={<SupportChat />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;

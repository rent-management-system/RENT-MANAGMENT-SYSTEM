import { jsx as _jsx, jsxs as _jsxs } from 'react/jsx-runtime';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { toast } from 'sonner';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';
import { Eye, EyeOff, Mail, Lock, User, Phone, UserCheck } from 'lucide-react';
const Register = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('tenant');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const { register, isLoading, error } = useAuth();
  const navigate = useNavigate();
  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast.error('Password Mismatch', {
        description: 'Passwords do not match. Please try again.',
      });
      return;
    }
    if (password.length < 6) {
      toast.error('Password Too Short', {
        description: 'Password must be at least 6 characters long.',
      });
      return;
    }
    const full_name = `${firstName} ${lastName}`;
    try {
      await register({
        full_name,
        email,
        password,
        phone_number: phoneNumber,
        role,
      });
      toast.success('Registration Successful', {
        description: 'Your account has been created successfully!',
      });
      navigate('/login');
    } catch (err: any) {
      console.error('Registration error:', err);
      if (err.response && err.response.data && err.response.data.detail) {
        console.error('Backend validation errors:', err.response.data.detail);
        toast.error('Registration Failed', {
          description: err.response.data.detail[0].msg || 'Please check your information and try again.',
        });
      } else {
        toast.error('Registration Failed', {
          description: error || 'Please check your information and try again.',
        });
      }
    }
  };
  const handleGoogleRegister = () => {
    window.location.href = `http://localhost:8001/auth/google`;
  };
  return _jsx('div', {
    className:
      'min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4',
    children: _jsxs(Card, {
      className:
        'w-full max-w-md shadow-2xl border-0 bg-white/80 backdrop-blur-sm',
      children: [
        _jsxs(CardHeader, {
          className: 'space-y-4 text-center pb-8',
          children: [
            _jsx('div', {
              className:
                'mx-auto w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center',
              children: _jsx(User, { className: 'h-8 w-8 text-white' }),
            }),
            _jsx(CardTitle, {
              className:
                'text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent',
              children: 'Create Account',
            }),
            _jsx(CardDescription, {
              className: 'text-gray-600 text-base',
              children: 'Sign up to get started with your account',
            }),
          ],
        }),
        _jsxs(CardContent, {
          className: 'space-y-6',
          children: [
            _jsxs('form', {
              onSubmit: handleRegister,
              className: 'space-y-5',
              children: [
                _jsxs('div', {
                  className: 'grid grid-cols-2 gap-4',
                  children: [
                    _jsxs('div', {
                      className: 'space-y-2',
                      children: [
                        _jsx(Label, {
                          htmlFor: 'firstName',
                          className: 'text-sm font-medium text-gray-700',
                          children: 'First Name',
                        }),
                        _jsxs('div', {
                          className: 'relative',
                          children: [
                            _jsx(User, {
                              className:
                                'absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400',
                            }),
                            _jsx(Input, {
                              id: 'firstName',
                              type: 'text',
                              placeholder: 'First name',
                              value: firstName,
                              onChange: (e) => setFirstName(e.target.value),
                              className:
                                'pl-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors',
                              required: true,
                            }),
                          ],
                        }),
                      ],
                    }),
                    _jsxs('div', {
                      className: 'space-y-2',
                      children: [
                        _jsx(Label, {
                          htmlFor: 'lastName',
                          className: 'text-sm font-medium text-gray-700',
                          children: 'Last Name',
                        }),
                        _jsxs('div', {
                          className: 'relative',
                          children: [
                            _jsx(User, {
                              className:
                                'absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400',
                            }),
                            _jsx(Input, {
                              id: 'lastName',
                              type: 'text',
                              placeholder: 'Last name',
                              value: lastName,
                              onChange: (e) => setLastName(e.target.value),
                              className:
                                'pl-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors',
                              required: true,
                            }),
                          ],
                        }),
                      ],
                    }),
                  ],
                }),
                _jsxs('div', {
                  className: 'space-y-2',
                  children: [
                    _jsx(Label, {
                      htmlFor: 'email',
                      className: 'text-sm font-medium text-gray-700',
                      children: 'Email Address',
                    }),
                    _jsxs('div', {
                      className: 'relative',
                      children: [
                        _jsx(Mail, {
                          className:
                            'absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400',
                        }),
                        _jsx(Input, {
                          id: 'email',
                          type: 'email',
                          placeholder: 'Enter your email',
                          value: email,
                          onChange: (e) => setEmail(e.target.value),
                          className:
                            'pl-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors',
                          required: true,
                        }),
                      ],
                    }),
                  ],
                }),
                _jsxs('div', {
                  className: 'space-y-2',
                  children: [
                    _jsx(Label, {
                      htmlFor: 'password',
                      className: 'text-sm font-medium text-gray-700',
                      children: 'Password',
                    }),
                    _jsxs('div', {
                      className: 'relative',
                      children: [
                        _jsx(Lock, {
                          className:
                            'absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400',
                        }),
                        _jsx(Input, {
                          id: 'password',
                          type: showPassword ? 'text' : 'password',
                          placeholder: 'Create a password',
                          value: password,
                          onChange: (e) => setPassword(e.target.value),
                          className:
                            'pl-10 pr-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors',
                          required: true,
                        }),
                        _jsx('button', {
                          type: 'button',
                          onClick: () => setShowPassword(!showPassword),
                          className:
                            'absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors',
                          children: showPassword
                            ? _jsx(EyeOff, { className: 'h-4 w-4' })
                            : _jsx(Eye, { className: 'h-4 w-4' }),
                        }),
                      ],
                    }),
                  ],
                }),
                _jsxs('div', {
                  className: 'space-y-2',
                  children: [
                    _jsx(Label, {
                      htmlFor: 'confirmPassword',
                      className: 'text-sm font-medium text-gray-700',
                      children: 'Confirm Password',
                    }),
                    _jsxs('div', {
                      className: 'relative',
                      children: [
                        _jsx(Lock, {
                          className:
                            'absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400',
                        }),
                        _jsx(Input, {
                          id: 'confirmPassword',
                          type: showConfirmPassword ? 'text' : 'password',
                          placeholder: 'Confirm your password',
                          value: confirmPassword,
                          onChange: (e) => setConfirmPassword(e.target.value),
                          className:
                            'pl-10 pr-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors',
                          required: true,
                        }),
                        _jsx('button', {
                          type: 'button',
                          onClick: () =>
                            setShowConfirmPassword(!showConfirmPassword),
                          className:
                            'absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors',
                          children: showConfirmPassword
                            ? _jsx(EyeOff, { className: 'h-4 w-4' })
                            : _jsx(Eye, { className: 'h-4 w-4' }),
                        }),
                      ],
                    }),
                  ],
                }),
                _jsxs('div', {
                  className: 'space-y-2',
                  children: [
                    _jsx(Label, {
                      htmlFor: 'role',
                      className: 'text-sm font-medium text-gray-700',
                      children: 'Role',
                    }),
                    _jsxs('div', {
                      className: 'relative',
                      children: [
                        _jsx(UserCheck, {
                          className:
                            'absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 z-10',
                        }),
                        _jsxs(Select, {
                          value: role,
                          onValueChange: setRole,
                          children: [
                            _jsx(SelectTrigger, {
                              className:
                                'pl-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors',
                              children: _jsx(SelectValue, {
                                placeholder: 'Select your role',
                              }),
                            }),
                            _jsxs(SelectContent, {
                              className:
                                'bg-white border border-gray-200 shadow-lg',
                              children: [
                                _jsx(SelectItem, {
                                  value: 'tenant',
                                  children: 'Tenant',
                                }),
                                _jsx(SelectItem, {
                                  value: 'owner',
                                  children: 'Owner',
                                }),
                                _jsx(SelectItem, {
                                  value: 'admin',
                                  children: 'Admin',
                                }),
                                _jsx(SelectItem, {
                                  value: 'broker',
                                  children: 'Broker',
                                }),
                              ],
                            }),
                          ],
                        }),
                      ],
                    }),
                  ],
                }),
                _jsxs('div', {
                  className: 'space-y-2',
                  children: [
                    _jsx(Label, {
                      htmlFor: 'phoneNumber',
                      className: 'text-sm font-medium text-gray-700',
                      children: 'Phone Number',
                    }),
                    _jsxs('div', {
                      className: 'relative',
                      children: [
                        _jsx(Phone, {
                          className:
                            'absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400',
                        }),
                        _jsx(Input, {
                          id: 'phoneNumber',
                          type: 'tel',
                          placeholder: 'Enter your phone number',
                          value: phoneNumber,
                          onChange: (e) => setPhoneNumber(e.target.value),
                          className:
                            'pl-10 h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors',
                        }),
                      ],
                    }),
                  ],
                }),
                _jsx(Button, {
                  type: 'submit',
                  disabled: isLoading,
                  className:
                    'w-full h-12 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]',
                  children: isLoading
                    ? _jsxs('div', {
                        className: 'flex items-center space-x-2',
                        children: [
                          _jsx('div', {
                            className:
                              'w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin',
                          }),
                          _jsx('span', { children: 'Creating account...' }),
                        ],
                      })
                    : 'Create Account',
                }),
              ],
            }),
            _jsxs('div', {
              className: 'relative',
              children: [
                _jsx('div', {
                  className: 'absolute inset-0 flex items-center',
                  children: _jsx('div', {
                    className: 'w-full border-t border-gray-200',
                  }),
                }),
                _jsx('div', {
                  className: 'relative flex justify-center text-sm',
                  children: _jsx('span', {
                    className: 'px-4 bg-white text-gray-500 font-medium',
                    children: 'Or continue with',
                  }),
                }),
              ],
            }),
            _jsxs(Button, {
              type: 'button',
              variant: 'outline',
              onClick: handleGoogleRegister,
              className:
                'w-full h-12 border-gray-200 hover:bg-gray-50 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]',
              children: [
                _jsxs('svg', {
                  className: 'w-5 h-5 mr-3',
                  viewBox: '0 0 24 24',
                  children: [
                    _jsx('path', {
                      fill: '#4285F4',
                      d: 'M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z',
                    }),
                    _jsx('path', {
                      fill: '#34A853',
                      d: 'M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z',
                    }),
                    _jsx('path', {
                      fill: '#FBBC05',
                      d: 'M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z',
                    }),
                    _jsx('path', {
                      fill: '#EA4335',
                      d: 'M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z',
                    }),
                  ],
                }),
                _jsx('span', {
                  className: 'text-gray-700 font-medium',
                  children: 'Sign up with Google',
                }),
              ],
            }),
            _jsxs('div', {
              className: 'text-center text-sm text-gray-600',
              children: [
                'Already have an account?',
                ' ',
                _jsx('button', {
                  onClick: () => navigate('/login'),
                  className:
                    'text-blue-600 hover:text-blue-700 font-semibold hover:underline transition-colors',
                  children: 'Sign in',
                }),
              ],
            }),
          ],
        }),
      ],
    }),
  });
};
export default Register;

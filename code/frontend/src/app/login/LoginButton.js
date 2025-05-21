'use client'

import { signIn } from 'next-auth/react'
import { Button } from '@/components/button'

export function LoginButton() {
    const handleLogin = () => {
        signIn('keycloak', {
            callbackUrl: '/',
        })
    }

    return (
        <Button
            className="mt-8 w-20"
            onClick={handleLogin}
        >
            Войти
        </Button>
    )
}
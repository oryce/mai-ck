'use client'

import { Button } from '@/components/button'
import { signIn } from 'next-auth/react'

export default function LoginButton() {
  return (
    <Button
      className="mt-8 w-20"
      onClick={() => signIn('keycloak', { callbackUrl: '/documents' })}
    >
      Войти
    </Button>
  )
}

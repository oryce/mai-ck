import NextAuth from 'next-auth'
import KeycloakProvider from 'next-auth/providers/keycloak'

async function refreshAccessToken(token) {
  try {
    const url = `${process.env.KC_INTERNAL_URL}/realms/${process.env.KC_REALM}/protocol/openid-connect/token`

    const params = new URLSearchParams({
      client_id: process.env.KC_CLIENT_ID,
      client_secret: process.env.KC_CLIENT_SECRET,
      grant_type: 'refresh_token',
      refresh_token: token.refreshToken,
    })

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    })

    const refreshed = await response.json()

    if (!response.ok) {
      throw refreshed
    }

    return {
      ...token,
      accessToken: refreshed.access_token,
      expiresAt: Date.now() + refreshed.expires_in * 1000,
      refreshToken: refreshed.refresh_token ?? token.refreshToken,
      idToken: refreshed.id_token,
    }
  } catch (error) {
    console.error('Error refreshing access token:', error)
    return {
      ...token,
      error: 'RefreshAccessTokenError',
    }
  }
}

export const authOptions = {
  providers: [
    KeycloakProvider({
      clientId: process.env.KC_CLIENT_ID,
      clientSecret: process.env.KC_CLIENT_SECRET,
      issuer: `${process.env.KC_EXTERNAL_URL}/realms/${process.env.KC_REALM}`,
      authorization: {
        params: { scope: 'openid profile offline_access' },
        url: `${process.env.KC_EXTERNAL_URL}/realms/${process.env.KC_REALM}/protocol/openid-connect/auth`,
      },
      jwks_endpoint: `${process.env.KC_INTERNAL_URL}/realms/${process.env.KC_REALM}/protocol/openid-connect/certs`,
      token: `${process.env.KC_INTERNAL_URL}/realms/${process.env.KC_REALM}/protocol/openid-connect/token`,
      userinfo: `${process.env.KC_INTERNAL_URL}/realms/${process.env.KC_REALM}/protocol/openid-connect/userinfo`,
    }),
  ],
  callbacks: {
    async jwt({ token, account, user }) {
      if (account && user) {
        return {
          ...token,
          accessToken: account.access_token,
          expiresAt: Date.now() + (account.expires_in ?? 0) * 1000,
          refreshToken: account.refresh_token,
          idToken: account.id_token,
        }
      }

      if (Date.now() < token.expiresAt) {
        return token
      }

      return await refreshAccessToken(token)
    },
    /** Make the `idToken` available in the client session */
    async session({ session, token }) {
      session.idToken = token.idToken
      session.error = token.error

      return session
    },
  },
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }

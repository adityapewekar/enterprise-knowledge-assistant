import { MsalGuardConfiguration, MsalInterceptorConfiguration } from "@azure/msal-angular";
import { BrowserCacheLocation, InteractionType, IPublicClientApplication, PublicClientApplication } from "@azure/msal-browser";
import { AZURE_CONFIG } from "../../environment";

export function MSALInstanceFactory(): IPublicClientApplication {
  return new PublicClientApplication({
    auth: {
      clientId: AZURE_CONFIG.CLIENT_ID,
      authority: 'https://login.microsoftonline.com/'+AZURE_CONFIG.TENANT_ID,
      redirectUri: "http://localhost:4200",
      postLogoutRedirectUri: "http://localhost:4200",
    },
    cache: {
      cacheLocation: BrowserCacheLocation.LocalStorage,
    },
  });
}

export function MSALInterceptorConfigFactory(): MsalInterceptorConfiguration {
  const protectedResourceMap = new Map<string, Array<string>>();
  protectedResourceMap.set("https://graph.microsoft.com/v1.0/me", ["user.read"]);

  return {
    interactionType: InteractionType.Redirect,
    protectedResourceMap,
  };
}

export function MSALGuardConfigFactory(): MsalGuardConfiguration {
  return {
    interactionType: InteractionType.Redirect,
    authRequest: {
      scopes: ["user.read"],
    },
    loginFailedRoute: "/login-failed",
  };
}

// Hand-authored. Gated and compiled by 15_native/build.py; never written by it.
//
// The reference is 08_components/cards/patterns/sign-in.html.

import SwiftUI
import AnindaTokens
import AnindaTokensUI
import AnindaComponents

/// Signing in: two fields, one primary action, and a way out that is not a dead end.
///
/// The sign-in-link button is `.quiet` rather than a link, because on a form the
/// alternative route is an ACTION and a caller reading it as a link would expect
/// navigation. The distinction is what a screen reader announces.
public struct AnindaSignInScreen: View {
    @State private var email = ""
    @State private var password = ""
    @State private var stayed = false
    @Environment(\.anindaTheme) private var theme

    public init() {}

    public var body: some View {
        let s = AnindaStyle(theme)
        return PatternPage {
            AnindaCard {
                VStack(alignment: .leading, spacing: AnindaSpace.s3) {
                    PatternHeading("Sign in")

                    // The content types are what let the platform's own password
                    // manager fill this in, which is the single most useful thing
                    // a sign-in screen can do for accessibility. They are guarded
                    // because the enumeration differs by platform: macOS has an
                    // AppKit content type with a different set of cases, and tvOS
                    // has no autocapitalisation control at all. Guarding is
                    // honest; dropping them to keep one code path would take the
                    // feature away from the platform most people sign in on.
                    AnindaInput("Email address") {
                        emailField
                    }

                    AnindaInput("Password") {
                        passwordField
                    }

                    AnindaCheckbox("Keep me signed in",
                                   hint: "Only on a machine you trust.",
                                   isOn: $stayed)

                    Button("Sign in") {}
                        .buttonStyle(AnindaButtonStyle(.primary))

                    Button("Send me a sign-in link instead") {}
                        .buttonStyle(AnindaButtonStyle(.quiet))
                }
            }
            .foregroundStyle(s.ink)
        }
    }

    @ViewBuilder
    private var emailField: some View {
        #if os(iOS) || os(visionOS)
        TextField("", text: $email)
            .textContentType(.emailAddress)
            .textInputAutocapitalization(.never)
            .keyboardType(.emailAddress)
            .modifier(AnindaInputSkin())
        #else
        TextField("", text: $email)
            .modifier(AnindaInputSkin())
        #endif
    }

    @ViewBuilder
    private var passwordField: some View {
        #if os(iOS) || os(visionOS)
        SecureField("", text: $password)
            .textContentType(.password)
            .modifier(AnindaInputSkin())
        #else
        SecureField("", text: $password)
            .modifier(AnindaInputSkin())
        #endif
    }
}

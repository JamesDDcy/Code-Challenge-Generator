import React from 'react';
import { SignedIn, SignedOut, UserButton } from '@clerk/clerk-react';
import { Outlet, Link, Navigate } from 'react-router-dom';

export function Layout() {
    return <div className='app-layout'>
        <header className='app-header'>
            <div className='header-content'>
                <h1>Code Challenge Generator</h1>
                <nav>
                    <SignedIn>
                        <Link to="/">Generate Challenge</Link>
                        <Link to="/history">History</Link>
                        <UserButton />
                    </SignedIn>
                </nav>
            </div>
        </header>

        <main className='app-main'>
            <SignedOut>
                {/* 'replace' just means to replace them in the curr window instead of a new tab */}
                <Navigate to="/sign-in" replace />
            </SignedOut>
            <SignedIn>
                {/* Outlet means that we pass whatever it is passed to the layout component and put it right here*/}
                {/* the '/' and '/history' */}
                <Outlet />
            </SignedIn>

        </main>
    </div>
}
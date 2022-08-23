use std::alloc::System;

#[global_allocator]
static A: System = System;

#[cfg(test)]
mod tests {
    use super::*;

    static HOME: &str = "/Users/iphands";

    #[test]
    fn it_does_squash_home_dir() {
        assert_eq!(squash_home(HOME, HOME), "~");
	assert_eq!(squash_home(HOME, "/Users/iphands/foo"), "~/foo");
    }

    #[test]
    fn it_does_not_squash_deep_home_dir() {
        assert_eq!(squash_home(HOME, "/foo/Users/iphands"), "/foo/Users/iphands");
	assert_eq!(squash_home(HOME, "/foo/Users/iphands/foo"), "/foo/Users/iphands/foo");
    }
}

fn squash_home(home: &str, full_path: &str) -> String {
    if full_path.starts_with(home) {
	return full_path.replace(&home, "~");
    }

    return full_path.to_string();
}

fn main() {
    let home = std::env::var("HOME");

    match std::env::var("PWD") {
        Ok(full_path) => {
            let path = match home {
                Ok(h) => squash_home(&h, &full_path),
                _ => full_path
            };

            if path.len() < 25 {
                print!("{}", path);
                return;
            }

            let mut output = String::new();
            let mut chars = path.chars();

            let limit = path.split("/").collect::<Vec<&str>>().len() - 2;

            if limit < 2 {
                print!("{}", path);
                return;
            }

            let mut count = 0;

            loop {
                // println!("{} {}", count, limit);

                match chars.next() {
                    Some(c) => {
                        if count < limit {
                            if c == '~' {
                                output.push(c);
                                continue;
                            }

                            if c == '/' {
                                output.push(c);
                                output.push(chars.next().unwrap());
                                count += 1;
                                continue;
                            }
                            continue;
                        }

                        output.push(c);
                    },
                    None => break
                }
            }
            print!("{}", output);
            // println!("{}", path)
        }
        _ => {
            print!("error")
        }
    }
}
